from tketool.lmc.prompts.prompt_controller import *
from tketool.lmc.lmc_linked import lmc_linked_model
from tketool.lmc.models import LLM_Plus, LLM_Buffer_Plus
from pydantic import BaseModel, create_model, Field
from langchain.output_parsers import PydanticOutputParser, BooleanOutputParser
from enum import Enum, EnumMeta
from typing import List, Dict, get_type_hints, Type


def parse_basic_type(type_str: str) -> Type:
    """
    解析并返回基本数据类型。
    """
    if type_str == "str":
        return str
    elif type_str == "int":
        return int
    elif type_str == "float":
        return float
    elif type_str == "bool":
        return bool
    else:
        raise ValueError(f"Unsupported basic type: {type_str}")


def parse_compound_type(type_str: str, models: dict) -> Type:
    """
    递归解析复合类型字符串，并返回相应的Python类型。
    """
    if type_str.startswith("List["):
        inner_type_str = type_str[len("List["):-1]
        return List[parse_type(inner_type_str, models)]
    elif type_str.startswith("Dict["):
        key_type_str, value_type_str = type_str[len("Dict["):-1].split(",")
        return Dict[parse_basic_type(key_type_str.strip()), parse_type(value_type_str.strip(), models)]
    else:
        # 对于非容器类型，尝试从models字典中获取对应的动态类型
        if type_str in models:
            return models[type_str]
        else:
            return parse_basic_type(type_str)


def parse_type(type_str: str, models: dict) -> Type:
    """
    解析类型字符串，返回对应的数据类型，支持嵌套和复合类型。

    :param type_str: 要解析的类型字符串。
    :param models: 包含所有动态模型或预定义类型的字典。
    :return: 对应的Python类型。
    """
    try:
        # 先尝试直接解析基础或已定义的复杂类型
        return parse_compound_type(type_str, models)
    except ValueError as e:
        print(f"Error parsing type '{type_str}': {e}")
        raise


class lmc_flow_result:
    def __init__(self):
        self.sub_process_logs = []
        self.results = []

    @property
    def result(self):
        if len(self.results) == 0:
            return None
        return self.results[0]

    @property
    def passed(self):
        return len(self.results) > 0


class lmc_linked_flow_model():
    def __init__(self, prompt_file: prompt_define_file, retry_time=3):

        self.type_parser_mapping = {
            "bool": BooleanOutputParser(),
        }

        self.define_file = prompt_file
        self.retry_time = retry_time

        all_models = {}

        self.enum_models = {}
        for k, enum_define in self.define_file.enums.items():
            # enum_type = self._create_enum(k, list(enum_define.enums_list.keys()))
            self.enum_models[k] = Enum(k, list(enum_define.enums_list.items()))  # list(enum_define.enums_list.keys())
            all_models[k] = self.enum_models[k]

        self.models = {}
        for k, define in self.define_file.models.items():
            field_dict = {}
            for f in define.fields_list:
                data_type = parse_type(f.field_type, all_models)
                # if f.field_type in self.enum_models:
                #     data_type = self.enum_models[f.field_type]
                # elif f.field_type in self.models:
                #     data_type = self.models[f.field_type]
                # elif f.field_sub_type:
                #     if f.field_type.lower() == "list":
                #         pass
                # else:
                #     data_type = eval(f.field_type)
                field_dict[f.field_name] = (data_type, Field(description=f.field_des))

            dynamic_model = create_model(k, **field_dict)
            self.models[k] = dynamic_model
            all_models[k] = dynamic_model

        self.linked_model = {}

        pass

    def _invoke_model(self, root_prompt_key, results, **kwargs, ):
        pointer = self.linked_model[root_prompt_key]
        p_define = self.define_file.prompts[root_prompt_key]
        last_result = None
        while True:
            result_stack = []
            cresult = pointer(last=last_result, **kwargs)
            results.sub_process_logs.append(cresult.process_logs)
            result_stack.append(cresult.result)

            if len(result_stack) > 0:
                last_result = result_stack[0]
                results.results.append(result_stack[0])

                if len(p_define.prompt_goto) > 0:
                    value_mapping = {}
                    default_to = None
                    for sub_p_k in p_define.prompt_goto:
                        if sub_p_k in self.define_file.prompts:
                            value_mapping[self.define_file.prompts[sub_p_k].prompt_condition_value] = sub_p_k

                        if self.define_file.prompts[sub_p_k].prompt_condition_default:
                            default_to = sub_p_k

                    if p_define.prompt_condition_field == "":
                        pointer = self.linked_model[p_define.prompt_goto[0]]
                        p_define = self.define_file.prompts[p_define.prompt_goto[0]]
                        continue

                    navigate_value = eval(f"last_result." + p_define.prompt_condition_field)
                    navigate_value = str(navigate_value)

                    if navigate_value in value_mapping:
                        pointer = self.linked_model[value_mapping[navigate_value]]
                        p_define = self.define_file.prompts[value_mapping[navigate_value]]
                        continue

                    if default_to:
                        pointer = self.linked_model[default_to]
                        p_define = self.define_file.prompts[default_to]
                        continue
                else:
                    break
            raise Exception("error in invoke flow.")

    def __call__(self, llm, **kwargs):

        for k, pro_def in self.define_file.prompts.items():
            if k in self.linked_model:
                continue

            output_type = pro_def.prompt_output.strip()
            li = lmc_linked_model(llm).set_prompt_template(pro_def.prompt_content).set_retry(self.retry_time)

            if pro_def.prompt_output in self.models:
                parser_out = PydanticOutputParser(pydantic_object=self.models[pro_def.prompt_output])
                li = li.set_output_parser(parser_out).set_output_fix()
            elif pro_def.prompt_output in self.enum_models:
                li = li.set_enum_output_parser(self.enum_models[pro_def.prompt_output]).set_output_fix()
            elif output_type in self.type_parser_mapping:
                parser_out = self.type_parser_mapping[output_type]
                li = li.set_output_parser(parser_out).set_output_fix()

            self.linked_model[k] = li

        root_prompt_key = 'default' if 'default' in self.linked_model else list(self.linked_model.keys())[0]

        results = lmc_flow_result()

        self._invoke_model(root_prompt_key=root_prompt_key, results=results,
                           **self.define_file.static_str_dict, **kwargs)

        return results
