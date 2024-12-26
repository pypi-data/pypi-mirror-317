import requests
import json
from tketool.lmc.models import LLM_Plus
from typing import Any, Optional
from tketool.logs import log


class BaiduAIModel(LLM_Plus):
    access_token: Optional[Any] = None
    url: Optional[str] = None
    client: Optional[Any] = None
    model_name: Optional[str] = None
    construct_query_invoker: Optional[Any] = None
    response_invoker: Optional[Any] = None

    def __init__(self, api_key, secret_key, model_name, price, call_method='api', config_file=None, **kwargs: Any):
        """
        调用百度千帆大模型平台下的大模型
        参数：
        - api_key、secret_key：模型调用的身份凭证，str, 获取方式：https://cloud.baidu.com/doc/WENXINWORKSHOP/s/flfmc9do2
        - model_name： 模型名称，str,可选ernie-3.5-8k、ernie-4.0-8k
        - price: 模型调用价格，元组 (输入价格，输出价格)
        - call_method: 模型调用方式，str,可选，api、sdk,默认为api调用
        - config_file: config文件路径
        """

        super().__init__(model_name, price=price, config_file_path=config_file, **kwargs)

        if not api_key and not self.config_obj:
            log('Baidu AI params must be given by config file or Parameter passing')

        if self.config_obj:
            api_key = self.config_obj.get_config("baidu_api_key", "not_set")
            secret_key = self.config_obj.get_config("baidu_secret_key", "not_set")
            model_name = self.config_obj.get_config('baidu_model_name', "not_set")

        self.model_name = self.model_name_map(model_name, call_method)

        self.call_method_select(call_method, api_key, secret_key)

    def call_method_select(self, call_method, api_key, secret_key):
        match call_method:
            case 'api':
                self.access_token = self.get_access_token(api_key, secret_key)
                self.url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{self.model_name.lower()}?access_token={self.access_token}"

                self.response_invoker = self._responese_invoker_api
                self.construct_query_invoker = self._construct_query_api

            case 'sdk':
                try:
                    import qianfan
                    self.client = qianfan.ChatCompletion(
                        ak=api_key,
                        sk=secret_key)
                except ImportError as e:
                    raise Exception(e)

                self.response_invoker = self._responese_invoker_sdk
                self.construct_query_invoker = self._construct_query

            case _:
                raise Exception(f"call method must be sdk or api, but '{call_method}'")

    @staticmethod
    def get_access_token(api_key, secret_key):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": api_key, "client_secret": secret_key}
        return str(requests.post(url, params=params).json().get("access_token"))

    @staticmethod
    def model_name_map(model_name, call_method):
        match model_name:
            case 'ernie-4.0-8k':
                match call_method:
                    case 'api': return 'completions_pro'
                    case 'sdk': return 'ERNIE-Bot-4'
                    case _: raise Exception(f"call method must be sdk or api, but '{call_method}'")
            case 'ernie-3.5-8k':
                match call_method:
                    case 'api': return 'completions'
                    case 'sdk': return 'ERNIE-Bot'
                    case _: raise Exception(f"call method must be sdk or api, but '{call_method}'")
            case _:
                return model_name

    @staticmethod
    def _construct_query(prompt):
        return [{'role': 'user', 'content': prompt}]

    def _construct_query_api(self, prompt):
        messages = self._construct_query(prompt)
        payload = json.dumps({
            "messages": messages,
            "disable_search": False,
            "enable_citation": False,
            # "response_format": "json_object", # result为str类型json，存在一定概率为非json
            **self.call_dictionary_config
        })

        return payload

    def _parse_result(self, answer, response):
        if response is None: return ''
        prompt_token_count = response['usage']['prompt_tokens']
        completion_token_count = response['usage']['completion_tokens']

        cost = self.calculate_cost(prompt_token_count, completion_token_count)

        return answer, cost

    def _responese_invoker_api(self, prompt):

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        text = requests.request("POST", self.url, headers=headers, data=prompt).text

        if isinstance(text, str):
            try:
                text = json.loads(text)
            except Exception as e:
                log(e)

        if not isinstance(text, dict):
            return None, None

        if 'error_code' in text:
            log(text['error_msg'])
            return None, None

        return text['result'], text

    def _responese_invoker_sdk(self, prompt):
        response = self.client.do(
            model=self.model_name,
            messages=prompt,
            **self.call_dictionary_config
        )

        return (response.body['result'], response) if response.code == 200 else (None, None)

    def call_model(self, prompt, return_detail, *args, **kwargs) -> Any:
        payload = self.construct_query_invoker(prompt)
        answer, response = self.response_invoker(payload)
        result, cost = self._parse_result(answer, response)

        if return_detail:
            return result, cost

        return result


class BaiDu_ERNIE_4(BaiduAIModel):
    def __init__(self, api_key=None, secret_key=None, call_method='api', config_file=None, **kwargs: Any):
        super().__init__(api_key, secret_key,
                         model_name='ernie-4.0-8k',
                         price=(0.12, 0.12),
                         call_method=call_method,
                         config_file=config_file,
                         **kwargs)


class BaiDu_ERNIE_35(BaiduAIModel):
    def __init__(self, api_key=None, secret_key=None, call_method='api', config_file=None, **kwargs: Any):
        super().__init__(api_key, secret_key,
                         model_name='ernie-3.5-8k',
                         price=(0.012, 0.012),
                         call_method=call_method,
                         config_file=config_file,
                         **kwargs)


class BaiDu_ERNIE_4_preview(BaiduAIModel):
    def __init__(self, api_key=None, secret_key=None, call_method='api', config_file=None, **kwargs: Any):
        super().__init__(api_key, secret_key,
                         model_name='ernie-4.0-8k-preview',
                         price=(0.12, 0.12),
                         call_method=call_method,
                         config_file=config_file,
                         **kwargs)