from tketool.lmc.models import LLM_Plus
import httpx
from typing import Optional, List, Dict, Mapping, Any
import requests, os


class LingYiWanWuModel(LLM_Plus):
    api_token: Optional[str] = None
    client: Optional[Any] = None
    base_url: Optional[str] = None

    def __init__(self, api_token, model_name, price, call_method='openai', base_url=None, config_file=None, **kwargs: Any):
        """
        参数：
        api_token： 调用模型的身份凭证，str，获取方式：https://open.bigmodel.cn/usercenter/apikeys
        model_name: 模型名称， str
        price: 调用模型价格，元组, （输入价格，输出价格）
        call_method: 调用模型的方式，str, 可选sdk、openai,默认sdk
        base_url： 调用模型的url路径，仅当call_method为openai时起作用
        config_file: config文件路径
        """

        super().__init__(model_name, price=price, config_file_path=config_file, **kwargs)

        if self.config_obj:
            self.api_token = self.config_obj.get_config("lingyiwanwu_api_key", "not_set")
        else:
            self.api_token = api_token

        self.call_method_select(call_method, base_url)

    def call_method_select(self, call_method, base_url):
        match call_method:
            case 'openai':
                try:
                    from openai import OpenAI

                    if not self.call_dictionary_config.get('do_sample', True):
                        raise Exception('param of do_sample for openai sdk must be True.')

                    self.client = OpenAI(
                        api_key=self.api_token,
                        base_url=base_url
                    )

                except ImportError as e:
                    raise Exception("无法导入openai, 请安装")

            case _:
                raise Exception(f"call method must be openai, but '{call_method}")

    def _construct_query(self, prompt):
        return [{'role': 'user', 'content': prompt}]

    def _responese(self, prompt):
        return self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt,
            **self.call_dictionary_config
        )

    def _parse_result(self, response):
        answer = response.choices[0].message.content
        prompt_token_count = response.usage.prompt_tokens
        completion_token_count = response.usage.completion_tokens

        cost = self.calculate_cost(prompt_token_count, completion_token_count)

        # self.add_token_use((prompt_token_count, completion_token_count))

        return answer, cost

    def call_model(self, prompt, return_detail, *args, **kwargs) -> Any:
        messages = self._construct_query(prompt)
        response = self._responese(messages)
        result, cost = self._parse_result(response)

        if return_detail:
            return result, cost
        else:
            return result


class Lingyiwanwu_Yi_Large(LingYiWanWuModel):
    def __init__(self, api_token=None, call_method='openai', config_file=None, **kwargs: Any):
        super().__init__(model_name="yi-large",
                         api_token=api_token,
                         price=(0.02, 0.02),
                         config_file=config_file,
                         base_url="https://api.lingyiwanwu.com/v1",
                         call_method=call_method,
                         **kwargs)
