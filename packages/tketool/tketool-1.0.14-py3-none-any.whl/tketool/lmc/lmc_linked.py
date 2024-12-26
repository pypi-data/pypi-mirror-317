# pass_generate
from langchain.llms.base import LLM

import tketool.logs
from tketool.lmc.models import LLM_Plus, LLM_Buffer_Plus
from langchain.schema.output_parser import BaseOutputParser
from langchain.output_parsers.enum import EnumOutputParser
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain.output_parsers import PydanticOutputParser
import re
from langchain.output_parsers import OutputFixingParser
from langchain.prompts import PromptTemplate
from tketool.logs import log
from enum import Enum


class linked_log:
    def __init__(self, title=""):
        self.log_title = title
        self.log_dict = {}
        self.invoke_model_count = 0
        self.detail_list = []

    def __str__(self):
        return self.log_title


# class linked_log_collections:
#     def __init__(self, logs: [linked_log]):
#         self.logs = logs
#
#         self.invoke_model_count = sum([lg.invoke_model_count for lg in self.logs])
#
#         self.cost = self.merge_dicts_sum_values(self.logs)
#
#     def merge_dicts_sum_values(self, logs):
#         result = {}
#         for log in logs:
#             for details in log.detail_list:
#                 for key, value in details.items():
#                     if isinstance(value, int) or isinstance(value, float):
#                         if key in result:
#                             result[key] += value
#                         else:
#                             result[key] = value
#
#         return result


class lmc_result:
    def __init__(self):
        self.process_logs = []
        self.results = []

    @property
    def result(self):
        if len(self.results) == 0:
            return None
        return self.results[0]


class lmc_linked_model():
    """
    `lmc_linked_model`是一个用于处理链式模型的类。
    
    这个类主要通过将一系列的处理函数添加到不同的函数列表中，来实现对模型的初始化、正常处理、异常处理以及完成后的处理。这样，可以方便地处理模型的各种状态，并通过日志记录处理过程中的各种信息。
    
    参数:
        llm (`LLM_Plus`): 需要处理的模型。
    
    属性:
        llm (`LLM_Plus`): 需要处理的模型。
        retry_count (`int`):重试次数。
        invoke_times (`int`): 调用次数。
        output_parser (`BaseOutputParser`): 输出解析器。
        fix_output_parser (`OutputFixingParser`): 修复输出的解析器。
        prompt_template (`PromptTemplate`): 提示模板。
        init_func_list (`list`): 初始化函数列表。
        norm_func_list (`list`): 正常处理函数列表。
        completed_func_list (`list`): 完成处理函数列表。
        exception_func_list (`list`): 异常处理函数列表。
    
    方法:
        在本类中，主要包含了一些设置方法，如设置重试次数、设置输出修复、设置调用次数、设置提示模板、设置输出解析器等。
        另外，还包含了一些私有方法，用于处理函数列表的调用、处理日志状态等。
    
    使用示例:
    ```python
        llm = LLM_Plus()  # 假设这是一个已经初始化的模型
        linked_model = lmc_linked_model(llm)
    
        linked_model.set_retry(3)  # 设置重试次数为3
        linked_model.set_times(2)  # 设置调用次数为2
    
        # 设置输出解析器
        output_parser = BaseOutputParser()  # 假设这是一个已经初始化的输出解析器
        linked_model.set_output_parser(output_parser)
    
        # 设置提示模板
        linked_model.set_prompt_template("Hello, {name}")
    
        # 使用该模型
        result, logs = linked_model(prompt="Hello, World")
    ```
    在这个示例中，我们首先创建了一个`lmc_linked_model`的实例，并设置了重试次数、调用次数、输出解析器和提示模板。然后，我们调用模型并得到结果和日志。
    
    注意: 使用本类需要有一定的python编程基础和对正则表达式、异常处理等有一定了解。在使用过程中，请确保传入的模型和解析器等都是正确初始化的。
    """

    def __init__(self, llm: LLM_Plus):
        """
        `lmc_linked_model`是一个类，用于处理和维护LLM_Plus模型的各种参数和功能。它可以记录和管理模型的调用次数，错误处理等。
        
        `__init__`方法是该类的初始化方法，主要负责初始化各种属性和参数。
        
        参数:
            llm: LLM_Plus对象，需要处理的模型。
        
        属性:
            retry_count: 重试次数，默认为1，表示模型运行出错时，重试的次数。
            invoke_times: 调用次数，默认为1，表示模型要调用的次数。
            output_parser: 输出解析器，用于解析模型的输出结果，默认为None。
            fix_output_parser: 修复输出解析器，用于处理模型的异常输出，默认为None。
            prompt_template: 提示模板，用于生成模型的输入，默认为None。
            init_func_list: 初始化函数列表，用于处理模型的初始化操作，默认为空列表[]。
            norm_func_list: 正常函数列表，用于存储处理模型正常运行的函数，默认为空列表[]。
            completed_func_list: 完成函数列表，用于处理模型运行完成后的操作，默认为空列表[]。
            exception_func_list: 异常函数列表，用于处理模型运行出错的情况，默认为空列表[]。
        
        在使用此类时，首先创建一个LLM_Plus对象，然后将其作为参数传递给lmc_linked_model的初始化方法来创建一个lmc_linked_model对象。然后可以通过这个对象来管理和操作模型，如设置重试次数、调用次数、解析器等。
        
        例如:
        ```python
        llm = LLM_Plus()
        lmc_model = lmc_linked_model(llm)
        lmc_model.set_retry(3).set_times(5)
        ```
        """

        self.llm = llm
        self.retry_count = 1
        self.invoke_times = 1
        self.output_parser = None
        self.fix_output_parser = None
        self.prompt_template = None
        self.init_func_list = []
        self.norm_func_list = []
        self.completed_func_list = []
        self.exception_func_list = []

        def model_invoke(ori_prompt, last_output, log):
            log.log_title = "invoke model"
            log.log_dict['prompt'] = last_output
            result, detail = self.llm(last_output, return_detail=True)
            log.invoke_model_count += 1
            log.detail_list.append(detail)
            log.log_dict['result'] = result
            # result = "##"
            return result

        self.norm_func_list.append(model_invoke)

    def set_retry(self, count):
        """
        设置重试次数。
        
        此方法用于设定模型在调用过程中出现异常时的重试次数。
        
        Args:
            count: 一个整数，表示重试的次数。
        
        Returns:
            返回当前的lmc_linked_model实例，以支持链式调用。
        
        示例:
            假设我们有一个lmc_linked_model实例model，我们想要设置它的重试次数为3次，可以这样操作：
                model.set_retry(3)
        """

        self.retry_count = count
        return self

    def _fix_output(self, output):
        """
        这个函数是用来修复输出的。将输出作为输入，尝试使用修复解析器来修复并输出结果。
        
        参数:
            output(str): 输出结果，需要被修复的字符串。
        
        返回:
            result : 返回通过fix_parser处理过的结果，如果处理过程中出现了异常，则返回None。
        
        示例:
            给定一个输出 "abc"，假设我们有一个修复解析器，它将所有的"a"替换为"b"，那么"_fix_output"函数将返回"bbc"。
        
        注意:
            如果在解析过程中抛出了异常，该函数会捕获异常并返回None，所以调用者需要对None做出正确的处理。
        """

        try:
            result = self.fix_parser.parse(output)
            return result
        except Exception as ex:
            return None

    def set_output_fix(self, donot_use_buffer=True):
        """
        这个函数的功能是设置输出修正。当`output_parser`被设置后，使用`OutputFixingParser.from_llm`生成一个修正输出的parser，并将其赋值给`fix_output_parser`。同时将一个名为`add_fix`的函数添加到`exception_func_list`列表中。这个`add_fix`函数的作用是使用`fix_output_parser`解析上一次的输出，并将解析结果返回。如果解析过程中抛出异常，函数将返回None。最后，函数返回自身以供链式操作。
        
        参数:
        无参数。
        
        返回:
        返回当前实例，支持链式操作。
        
        举例:
        ```python
        model = LMC_Linked_Model(...)
        model.set_output_fix()
        ```
        注意事项:
        在调用此函数前，必须要先设置`output_parser`，否则会抛出异常。
        """

        if self.output_parser is None:
            raise Exception("have not set the output parser.")

        fix_lm = self.llm
        if donot_use_buffer and isinstance(fix_lm, LLM_Buffer_Plus):
            fix_lm = self.llm.base_llm

        self.fix_output_parser = OutputFixingParser.from_llm(parser=self.output_parser, llm=fix_lm)

        def add_fix(ori_prompt, last_output, log):
            log.log_title = 'output_fix'
            log.log_dict['parser_name'] = type(self.fix_output_parser).__name__
            log.log_dict['last_output'] = last_output

            result = self.fix_output_parser.parse(last_output)

            log.invoke_model_count += 1
            log.detail_list.append(self.fix_output_parser.retry_chain.llm.get_last_detail())

            log.log_dict['parsed_result'] = result
            return result

        self.exception_func_list.append(add_fix)

        return self

    def set_times(self, count):
        """
            此方法用于设置模型调用的次数。
        
            Args:
                count (int): 指定的模型调用次数。
        
            Returns:
                self: 返回类的实例。
        
            示例:
                linked_model = lmc_linked_model(llm)
                linked_model.set_times(5) # 设置模型调用次数为5次
        
            注意:
                输入的次数应为正整数，否则可能会导致程序错误。
        """

        self.invoke_times = count
        return self

    def set_prompt_template(self, temp_str):
        """
        这个方法是为了设置提示模板。提示模板是根据模板字符串生成的，其中大括号包围的部分会被替换为对应的输出值。
        
        参数:
            temp_str: 字符串类型，用于定义提示模板的模板字符串。其中的大括号部分（如"{something}"）将被替换为对应的输出值。
        
        返回:
            返回当前对象自身，以便于链式调用。
        
        使用示例:
            lmc_linked_model_obj.set_prompt_template("The output is {output}")
        
        注意事项:
            请确保模板字符串中的大括号部分对应的key在模型的输出中确实存在，否则在模板字符串的填充过程中会出错。
        """

        def _find_bracket_words(s):
            # 使用正则表达式找出所有大括号内的词语
            words = re.findall(r'\{(.*?)\}', s)

            # 去重并输出
            return list(set(words))

        def prompt_temp(ori_prompt, last_output, log):
            if self.prompt_template is None:
                template_str = temp_str
                template_vars = _find_bracket_words(temp_str)
                template_partial_vars = {}
                if self.output_parser is not None:
                    template_str += "\n{format_instructions}"
                    template_partial_vars['format_instructions'] = self.output_parser.get_format_instructions()
                self.prompt_template = PromptTemplate(
                    template=template_str,
                    input_variables=template_vars,
                    partial_variables=template_partial_vars
                )

            # validate _input
            for v_input in self.prompt_template.input_variables:
                if v_input not in last_output:
                    last_output[v_input] = ""

            log.log_title = "prompt template generic."
            prompt = self.prompt_template.format(**last_output)
            log.log_dict['prompt'] = prompt
            return prompt

        self.init_func_list.append(prompt_temp)

        return self

    def set_output_parser(self, out_paser: BaseOutputParser):
        """
        设置用于解析输出结果的解析器。
        
        该函数主要用于设置解析器，用于提取模型输出结果中所需要的信息。通过这个函数，用户可以设置自定义的解析器，处理从模型返回的结果。
        
        参数:
            out_parser (BaseOutputParser): 用户自定义的解析器，需要继承自BaseOutputParser基类。
        
        返回:
            self，以便于链式调用其他方法。
        
        示例:
            # 创建一个自定义解析器
            class MyOutputParser(BaseOutputParser):
                def parse(self, output):
                    ...
            # 在模型中设置这个解析器
            my_model.set_output_parser(MyOutputParser())
        
        注意:
            如果已经设置过解析器，再次调用该方法会引发异常。在这种情况下，需要先清除已有的解析器，再设置新的解析器。
        """

        if self.output_parser is not None:
            raise Exception("more than one parser has been set.")

        self.output_parser = out_paser

        def add_parser(ori_prompt, last_output, log):
            log.log_title = "set_output_parser"
            log.log_dict['parser_name'] = type(out_paser).__name__
            log.log_dict['last_output'] = last_output
            result = out_paser.parse(last_output)
            log.log_dict['parsed_result'] = result
            return result

        self.norm_func_list.append(add_parser)

        return self

    def set_enum_output_parser(self, enum_or_list):
        """
        此函数用于设置枚举输出解析器。该函数接收一个枚举对象或列表作为参数，之后根据参数类型创建并设置对应的枚举输出解析器。
        
        参数:
            enum_or_list (Enum或list): 用于创建输出解析器的枚举对象或列表。如果参数是枚举对象，则直接使用该枚举对象创建解析器。如果参数是列表，则首先将列表转换为枚举对象，然后使用新的枚举对象创建解析器。
        
        返回:
            None
        
        使用示例:
            # 使用枚举对象设置解析器
            lmc_model.set_enum_output_parser(MyEnum)
        
            # 使用列表设置解析器
            lmc_model.set_enum_output_parser(['option1', 'option2', 'option3'])
        
        注意:
            如果enum_or_list既不是枚举对象也不是列表，则此函数会抛出异常。
        """

        if isinstance(enum_or_list, Enum):
            enums_items = [item.name for item in enum_or_list]
            enums = Enum('output_parse_enum', {item: item for item in enums_items})
            # enums = names
        elif isinstance(enum_or_list, list):
            enums = Enum('output_parse_enum', {item: item for item in enum_or_list})
        else:
            raise Exception("enum_or_list must be enum or list[str]")
        # parser = PydanticOutputParser(pydantic_object=enums)
        parser = EnumOutputParser(enum=enums)

        return self.set_output_parser(parser)

    def set_dictionary_output_parser(self, list_of_keys_tuple: [tuple]):
        """
        这个函数是为了设置字典类型的输出解析，参数是一个键的元组列表，每个元组包含两部分：键的名称和键的描述。
        
        函数会根据参数生成一系列的响应模式，然后基于这些响应模式生成一个结构化的输出解析器。
        
        对于一个包含复杂字典类型的输出，这个函数可以帮助解析输出并将其转化成结构化的形式以方便进一步处理。
        
        参数:
            list_of_keys_tuple: 一个元组列表，每个元组包含两部分：键的名称和键的描述。
        返回:
            此函数没有返回值，但是会将新生成的解析器设置为self.output_parser。
        
        示例：
            set_dictionary_output_parser([("name", "姓名"), ("age", "年龄")])
        这个样例代码会生成一个解析器，用于解析包含"name"和"age"两个字段的字典，"name"字段的描述是"姓名"，"age"字段的描述是"年龄"。
        """

        response_schemas = [
            ResponseSchema(name=kk, description=disc)
            for kk, disc in list_of_keys_tuple
        ]
        parser = StructuredOutputParser.from_response_schemas(response_schemas)

        return self.set_output_parser(parser)

    def set_pydantic_output_parser(self, pydantic_object):
        """
        这个方法是为了设置pydantic的输出解析器。pydantic是一个数据验证库，可以用于从复杂的数据类型中解析数据。
        
        参数:
            pydantic_object: pydantic的模型对象，其实例的输出将被用作解析器的目标。
        
        例子:
            该方法与PydanticOutputParser类一起使用，接受一个pydantic模型对象，然后使用该模型对象的实例来解析输出。
        
            ```python
            class UserModel(pydantic.BaseModel):
                name: str
                age: int
        
            lmc_model = lmc_linked_model(some_llm_model)
            lmc_model.set_pydantic_output_parser(UserModel)
            ```
        
        在上述示例中，用户创建了一个pydantic模型UserModel，这个模型有两个字段：name和age。然后在lmc_linked_model实例lmc_model中，调用set_pydantic_output_parser方法，将UserModel作为参数传入。这将设置lmc_model使用UserModel来解析其输出。
        
        返回值:
            该方法返回调用它的对象本身，以支持链式调用。
        
        注意:
            这个方法不会检查pydantic_object是否真的是pydantic的模型对象，如果传入非pydantic模型对象，可能会在运行时出现错误。
        
        错误处理:
            如果在运行时发生错误，通常是由于传入非pydantic模型对象或者模型对象的结构与输出数据不匹配引起的，这种情况下，错误消息将指向具体的问题，用户需要根据错误消息进行调整。
        """

        parser = PydanticOutputParser(pydantic_object=pydantic_object)
        return self.set_output_parser(parser)

    def _invoke_list_func(self, ori_input, history_output_list, log_list, func_list):
        """
        _invoke_list_func是一个私有的实例方法，它用于调用一系列给定的函数，并记录每个函数的输出和日志。

        参数:
        ori_input: 原始输入，用作每个函数的第一个参数。
        history_output_list: 历史输出列表，用于存储每个函数的输出。每个函数的第二个参数将是列表中的最后一个输出。
        log_list: 日志列表，用于存储每个函数的日志。
        func_list: 函数列表，这是要被调用的函数列表。

        返回：
        如果所有函数都成功执行，则返回None。否则，返回引发异常的第一个函数的异常实例。

        注意：本函数不会捕获并处理函数引发的异常，而是直接将异常返回。

        示例：
        def add_one(ori_input, last_output, log):
            log['operation'] = 'add one'
            return last_output + 1

        def multiply_two(ori_input, last_output, log):
            log['operation'] = 'multiply two'
            return last_output * 2

        history_output_list = [1]
        log_list = []

        _invoke_list_func(1, history_output_list, log_list, [add_one, multiply_two]) -> None
        assert history_output_list == [1, 2, 4]
        assert log_list == [{'operation': 'add one'}, {'operation': 'multiply two'}]
        """

        try:
            for fc in func_list:
                log = linked_log()
                log_list.process_logs.append(log)
                last_output = history_output_list[-1]
                last_output = fc(ori_input, last_output, log)
                history_output_list.append(last_output)

            return None
        except Exception as ex:
            log = linked_log()
            log.log_title = str(ex)
            log_list.process_logs.append(log)
            return ex

    def __call__(self, **kwargs):

        result = lmc_result()
        # result_list = []
        init_result_list = []
        init_result_list.append(kwargs)

        invoke_result = self._invoke_list_func(kwargs, init_result_list, result, self.init_func_list)
        if invoke_result is not None:
            raise invoke_result

        for time_idx in range(self.invoke_times):
            # log_dic_list = []
            for retry_id in range(self.retry_count):
                result.process_logs.append(linked_log(f"invoke time:{time_idx}, retry:{retry_id}"))
                middle_result_list = [init_result_list[-1]]

                normal_invoke_result = self._invoke_list_func(kwargs, middle_result_list, result,
                                                              self.norm_func_list)

                if normal_invoke_result is None:
                    result.results.append(middle_result_list[-1])
                    break

                if len(self.exception_func_list) == 0:
                    log = linked_log((f"invoke time:{time_idx}, retry:{retry_id} failed."))
                    log.log_dict = {
                        "error_time": f"time:{time_idx},retry:{retry_id},normal_invoke",
                        "error_msg": str(normal_invoke_result)
                    }
                    result.process_logs.append(log)
                    continue

                tketool.logs.log(f"invoke time:{time_idx}, retry:{retry_id} failed, run fix...")
                result.process_logs.append(linked_log(f"invoke time:{time_idx}, retry:{retry_id} failed, run fix..."))

                exception_invoke_result = self._invoke_list_func(kwargs, middle_result_list, result,
                                                                 self.exception_func_list)

                if exception_invoke_result is None:
                    result.results.append(middle_result_list[-1])
                    break
                else:
                    log = linked_log(
                        f"invoke time:{time_idx}, retry:{retry_id} failed, run fix failed. ex_msg: {str(exception_invoke_result)}")
                    log.log_dict = {
                        "error_time": f"time:{time_idx},retry:{retry_id},exception_invoke",
                        "error_msg": str(exception_invoke_result)
                    }

        self._invoke_list_func(kwargs, result.results, result, self.completed_func_list)

        return result
