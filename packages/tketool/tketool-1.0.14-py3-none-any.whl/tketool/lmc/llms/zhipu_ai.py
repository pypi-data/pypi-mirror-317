from tketool.lmc.models import LLM_Plus
import httpx
from typing import Optional, List, Dict, Mapping, Any
import requests, os


class ChatGLM_local(LLM_Plus):
    """
    这是一个名为`ChatGLM`的类，该类继承自基类`LLM_Plus`。该类主要用于实现和外部模型交互的API请求功能。

    主要包含三个方法：`__init__`，`_post` 和 `call_model`。

    `__init__`方法用于初始化ChatGLM类的实例。需要传入一个url字符串参数（用于API调用的url）和`**kwargs`参数（用于传入模型的其他参数）。

    `_post`方法用于向指定的url发送post请求。传入的参数包括一个url字符串和一个包含请求内容的字典。

    `call_model`方法用于调用模型。传入的参数包括一个prompt字符串（作为模型的输入）和其他可选的参数。该方法会对模型的返回结果进行处理，如果请求成功返回模型的预测结果，否则返回错误信息。

    类的使用示例：

    ```python
    chat_glm = ChatGLM("your_url")
    prompt = "你好，世界"
    result = chat_glm.call_model(prompt)
    # 返回模型的预测结果或错误信息
    print(result)
    ```

    注意：响应时间取决于模型的处理速度和网络状况，请在使用时确保网络通畅，以便及时获取请求结果。
    """

    gurl: str = ""

    def __init__(self, _url, **kwargs: Any):
        """
            这是ChatGLM类的初始化函数，用于初始化该类的实例。

            本方法首先通过调用父类的初始化方法，初始化LLM_Plus类，并设置模型的名称为"GLM6B"；
            然后，设置类变量gurl的值为参数_url，该变量将被用于后续的网络请求。

            Args:
                _url (str): 用于网络请求的URL地址
                **kwargs (Any): 可接收任何关键字参数，这些参数会被传递给父类LLM_Plus的初始化方法

            例子:

            ```
                chat_glm = ChatGLM(_url="http://example.com", token="my_token")
            ```

            在此例子中，我们创建了一个ChatGLM的实例，_url参数设置为"http://example.com"，
            并且通过kwargs传递了一个名为token的参数值为"my_token"到父类LLM_Plus的初始化方法中。
        """

        model_name = "GLM6B"
        super().__init__(model_name, **kwargs)
        self.gurl = _url

    def _post(self, url: str,
              query: Dict) -> Any:
        """
        这是一个私有的_post方法，用于向服务器发送POST请求。

        参数:
        url: str, 服务器的URL地址。
        query: Dict, 要发送的数据，以字典形式存在。

        返回:
        Any, 返回服务器的响应。

        使用方法:

        _post方法通常在类的内部使用，作为向服务器发送请求的工具函数。该函数使用了requests库的session对象进行网络请求，
        在请求过程中，设置了请求头为"Content_Type": "application/json"，并对请求进行了60秒的超时设置。
        在请求成功后，该函数返回服务器的响应。

        例如：
        假设我们有一个名为'query'的字典，包含我们要发送的数据。我们可以这样调用_post方法：

        response = self._post(url="http://example.com", query=query)

        注意：
        由于这是一个私有方法，所以通常只在类的内部使用。在类的外部调用可能会引发错误。
        """

        _headers = {"Content_Type": "application/json"}
        with requests.session() as sess:
            resp = sess.post(url,
                             json=query,
                             headers=_headers,
                             timeout=60)

        return resp

    def call_model(self, prompt, *args, **kwargs) -> Any:
        """
        这个方法是ChatGLM类的一部分，用于调用模型并获取预测结果。

        参数:
            prompt (str): 输入的提示，模型将根据该提示生成预测结果。
            *args: 变长参数，根据需要使用。
            **kwargs: 变长关键字参数，可以传递任意数量的关键字参数。

        返回:
            predictions (Any): 如果请求成功（HTTP状态码为200），则返回模型的预测结果；否则返回错误提示信息"请求模型Error"。

        使用示例:

        ```python
            glm = ChatGLM(_url='http://localhost:8000')
            prompt = "你好"
            print(glm.call_model(prompt))
        ```
        """

        query = {
            "prompt": prompt,
            "history": []
        }
        # post
        resp = self._post(url=self.gurl,
                          query=query)

        if resp.status_code == 200:
            resp_json = resp.json()
            predictions = resp_json["response"]

            return predictions
        else:
            return "请求模型Error"


class ZhipuGLMModel(LLM_Plus):
    api_token: Optional[str] = None
    client: Optional[Any] = None

    def __init__(self, api_token, model_name, price, call_method='sdk', base_url=None, config_file=None, **kwargs: Any):
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
            self.api_token = self.config_obj.get_config("zhipu_glm_token", "not_set")
        else:
            self.api_token = api_token

        self.call_method_select(call_method, base_url)

    def call_method_select(self, call_method, base_url):
        match call_method:
            case "sdk":
                try:
                    # 尝试导入非必需的包
                    from zhipuai import ZhipuAI

                    self.client = ZhipuAI(
                        api_key=self.api_token
                    )

                except ImportError as e:
                    # 如果导入失败，抛出一个异常或者打印一个错误消息
                    raise Exception("无法导入 zhipuai, 请安装")

            case 'openai':
                try:
                    from openai import OpenAI

                    self.client = OpenAI(
                        api_key=self.api_token,
                        base_url=base_url
                    )

                except ImportError as e:
                    raise Exception("无法导入openai, 请安装")

            case _:
                raise Exception(f"call method must be sdk or openai, but '{call_method}")

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


class Zhipu_GLM_4(ZhipuGLMModel):
    def __init__(self, api_token=None, call_method='sdk', config_file=None, **kwargs: Any):
        super().__init__(model_name="glm-4",
                         api_token=api_token,
                         price=(0.1, 0.1),
                         config_file=config_file,
                         base_url="https://open.bigmodel.cn/api/paas/v4/",
                         call_method=call_method,
                         **kwargs)
