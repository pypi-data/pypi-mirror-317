import httpx
from typing import Optional, List, Dict, Mapping, Any
from tketool.lmc.models import LLM_Plus
import requests, os
from openai import AsyncClient, AsyncOpenAI, OpenAI


class OpenAI_Complete_Model(LLM_Plus):
    """
    OpenAI_Complete_Model类是一个继承自LLM_Plus的类，用于实现与OpenAI对话模型的交互。在初始化时，它会根据提供的api token和模型名称初始化OpenAI客户端。这个类主要包含五个方法：`_construct_query`、`_invoke_model`、`_parse_invoke_result`、`call_model` 和`add_token_use`。

    类初始化方法`__init__`:
    - 参数:
        - `apitoken`(str): OpenAI的API认证令牌。
        - `model_name`(str): OpenAI模型的名称。
        - `price`(float): 调用模型的价格。
        - `base_url`(str): 调用模型的url路径
        - `**kwargs`(dict): 其他任意的关键字参数。
    - 返回: None

    方法`_construct_query`:
    - 功能: 构造一个查询请求，用于进一步向模型发送。
    - 参数:
        - `prompt`(str): 用户给模型的提示或问题。
    - 返回: 构造好的查询请求列表。

    方法`_invoke_model`:
    - 功能: 使用OpenAI客户端调用聊天模型，并返回响应。
    - 参数:
        - `prompt`(str): 用户给模型的提示或问题。
    - 返回: OpenAI聊天模型的响应。

    方法`_parse_invoke_result`:
    - 功能: 解析模型响应，获取并返回模型的回答，并记录消耗的token数。
    - 参数:
        - `response`(dict): OpenAI聊天模型的响应。
    - 返回: 模型的回答。

    方法`call_model`:
    - 功能: 调用上述三个方法，完成从构造请求到获取模型回答的整个过程。
    - 参数:
        - `prompt`(str): 用户给模型的提示或问题。
        - `*args`(tuple): 其他任意位置参数。
        - `**kwargs`(dict): 其他任意的关键字参数。
    - 返回: 模型的回答。

    使用例子：
    ```python
    model = OpenAI_Complete_Model(token, 'text-davinci-002', 0.06)
    prompt = 'Translate the following English text to French: {}'
    result = model.call_model(prompt.format('Hello, World!'))
    print(result)
    ```
    """

    api_token: Optional[str] = None
    proxy: Optional[str] = None
    client: Optional[OpenAI] = None
    base_url: Optional[str] = None

    def __init__(self, model_name, price, apitoken=None, proxy=None, base_url=None,  config_file=None,
                 **kwargs: Any):
        """
        这是一个初始化OpenAI_Complete_Model类的方法。该类继承自LLM_Plus类，用于与OpenAI API进行交互，获取模型预测的结果。

        初始化方法需要用户提供API的token，模型名称，以及模型的价格。

        如果用户希望使用代理，可以通过关键字参数proxy来设置。

        参数:

            apitoken: OpenAI平台的API token，类型为字符串，用于API调用的身份验证。

            model_name: OpenAI平台的模型名称，类型为字符串，指定调用哪个模型。

            price: 模型的价格，类型为数字，用于计算使用模型的费用。

            base_url: 调用模型的url路径，str

            **kwargs: 任意额外的关键字参数，可能包括代理设置，传给父类LLM_Plus的初始化方法。

        返回：

            无返回值。

        示例1:

            model = OpenAI_Complete_Model('gpt-4', (0.1, 0.15), 'API_TOKEN',proxy='http://localhost:8080')
            result = model.call_model('Hello, World!')

        示例2：
            model = OpenAI_Complete_Model('meta/llama3-70b-instruct', (0, 0), 'API_TOKEN', 'https://integrate.api.nvidia.com/v1', 'nvidia', proxy='http://localhost:8080')
            result = model.call_model('Hello, World!')

        注意事项：

            在使用代理时，需要保证代理的可用性和安全性，否则可能会影响API的调用和结果。
        """

        super().__init__(model_name, price=price, config_file_path=config_file, **kwargs)  # (0.03, 0.06)

        if self.config_obj:
            self.parse_config_obj(base_url)
        else:
            self.api_token = apitoken
            self.proxy = proxy
            self.base_url = base_url

        http_client = None
        if self.proxy is not None:
            http_client = httpx.Client(
                proxies=self.proxy
            )

        self.client = OpenAI(
            api_key=self.api_token,
            http_client=http_client,
            base_url=self.base_url
        )

    def parse_config_obj(self, base_url):
        self.proxy = self.config_obj.get_config("openai_proxy", "not_set")
        self.api_token = self.config_obj.get_config("openai_token", "not_set")
        self.base_url = base_url

    def _construct_query(self, prompt: str) -> List:
        """
        这个方法是用于构建查询的。在OpenAI Complete模型中，查询是以一个列表的形式存在的，列表中的元素是一个字典，键为'role'和'content'。'role'是一个字符串，表示发送消息的角色，这里是'user'，'content'是一个字符串，表示用户输入的提示。

        参数:
        prompt: str类型，表示用户输入的提示。

        返回:
        返回一个列表，列表中的元素是一个字典，键为'role'和'content'。

        示例:
        ```python
        def _construct_query(self, "你好"):
            # 返回: [{"role": "user", "content": "你好"}]
        ```
        """

        query = [
            {"role": "user", "content": prompt}
        ]
        return query

    def _invoke_model(self, prompt):
        """
        该函数用于调用模型并获取响应。

        参数:
            prompt: str类型，传入的用户提示信息。

        返回:
            返回从OpenAI接口获取的响应结果，通常是模型生成的文本结果。

        在此函数中，我们使用了OpenAI的chat.completions.create接口来调用我们的模型。我们将用户的提示信息（prompt）传入模型，并将模型的响应结果返回。返回的结果将在后续的_parse_invoke_result函数中进行解析。
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=prompt,
            **self.call_dictionary_config
        )

        return response

    def _parse_invoke_result(self, response):
        """
            此函数的目的是解析模型调用的响应，并从响应中抽取所需的信息。

            该函数首先从响应中获取答案内容。接着，它获取输入（prompt）和补全所用的令牌（token）数量。最后，它会添加令牌的使用情况并返回答案。

            参数:
            response: OpenAI的模型调用响应。它是一个包含模型生成的文本、令牌的数量等信息的对象。

            返回:
            返回从响应中获取的答案内容，它是一个字符串。

            注意:
            这个函数没有错误处理机制，如果响应的结构与预期不符，可能会引发异常。例如，如果响应中没有"choices"键，将无法获取到答案内容。
        """

        answer = response.choices[0].message.content

        prompt_token_count = response.usage.prompt_tokens
        completion_token_count = response.usage.completion_tokens

        cost = self.calculate_cost(prompt_token_count, completion_token_count)
        # self.add_token_use((prompt_token_count, completion_token_count))

        return answer, cost

    def call_model(self, prompt, return_detail, *args, **kwargs) -> Any:
        """
        该函数是模型类OpenAI_Complete_Model的一个方法，用于调用模型并返回模型的输出结果。

        参数:
            prompt (str): 用户的输入提示，模型将基于此提示生成相应的回答或完成相应的任务。
            *args: 可变参数，根据具体需要传入。
            **kwargs: 关键字参数，根据具体需要传入。

        返回:
            Any: 返回模型生成的回答或完成任务的结果。

        用法示例:
            model = OpenAI_Complete_Model(apitoken="your_api_token", model_name="gpt-3", price=0.05)
            result = model.call_model(prompt="Translate the following English text to French: '{}'", *args, **kwargs)

        注意:
            在使用该函数时，需要确保已经正确设置了OpenAI的API密钥，并且已经选择了正确的模型。
        """

        query = self._construct_query(prompt)
        invoke_result = self._invoke_model(query)
        result, cost = self._parse_invoke_result(invoke_result)

        if return_detail:
            return result, cost
        else:
            return result


class Openai_ChatGPT_4(OpenAI_Complete_Model):
    """
    ChatGPT4是一个继承自OpenAI_Complete_Model的类，用于创建并管理OpenAI的GPT-4聊天模型的实例。

    这个类的主要目的是使用OpenAI的API，利用提供的API令牌，实现与GPT-4聊天模型的交互。

    示例：

    ```python
    # 使用API令牌初始化ChatGPT4实例
    chatgpt = ChatGPT4(apitoken='your_openai_api_token')

    # 使用ChatGPT4实例进行一些操作，例如生成文本
    generated_text = chatgpt.generate_text(input_text='Hello, world!')
    ```

    参数:

    - `apitoken`: OpenAI的API令牌，是一个字符串，用于进行身份验证和API访问。
    - `kwargs`: 其他可选参数，可以传递给OpenAI_Complete_Model的初始化方法。

    注意：

    - 请确保你的OpenAI API令牌是有效的，否则将无法使用GPT-4模型。
    - 这个类没有明确的返回类型，它的主要作用是创建和管理GPT-4模型的实例。
    """

    def __init__(self, apitoken=None, proxy=None, config_file=None, **kwargs: Any):
        """
        初始化ChatGPT4类的实例。

        这个类是OpenAI_Complete_Model的子类，用于创建和管理GPT-4模型的实例。通过这个类，我们可以方便地调用和使用OpenAI的GPT-4模型进行各种任务。这个类在初始化时需要传入OpenAI的API令牌，这样才能正确地使用模型。

        参数：
            apitoken (str): OpenAI的API令牌，用于验证用户身份和调用模型。
            **kwargs: 任意关键字参数，这些参数将直接传递给OpenAI_Complete_Model的构造函数。

        例子：
            >>> model = ChatGPT4('YOUR_OPENAI_TOKEN')
            >>> output = model.generate_prompt('Hello, world')

        注意：
            请确保你的OpenAI API令牌是正确的，错误的令牌可能会导致无法调用模型。
            当前版本的类并不支持修改GPT-4模型的配置，模型的temperature和max tokens是固定的。

        """

        super().__init__(model_name="gpt-4", apitoken=apitoken, price=(0.03, 0.06), config_file=config_file,
                         proxy=proxy, **kwargs)


class Openai_ChatGPT_4_Turbo(OpenAI_Complete_Model):

    def __init__(self, apitoken=None, proxy=None, config_file=None, **kwargs: Any):
        super().__init__(model_name="gpt-4-turbo", apitoken=apitoken, price=(0.01, 0.03),
                         config_file=config_file,
                         proxy=proxy, **kwargs)


class ChatGPT4_omni(OpenAI_Complete_Model):

    def __init__(self, apitoken=None, proxy=None, config_file=None, **kwargs: Any):
        super().__init__(model_name="gpt-4o", apitoken=apitoken, price=(0.005, 0.015),
                         config_file=config_file,
                         proxy=proxy, **kwargs)


class Openai_ChatGPT_3(OpenAI_Complete_Model):
    """
    这是一个继承自OpenAI_Complete_Model的聊天模型类ChatGPT3。主要用于实现和Gpt-3.5的交互，包括生成文本等。

    参数:
    apitoken: API访问密钥。用于验证和建立与OpenAI模型的连接。
    **kwargs: 可以接受任意关键字参数。这些参数将传递给父类。

    使用示例:
    ```python
    apitoken = "你的API密钥"
    model = ChatGPT3(apitoken)
    generated_text = model.generate("你想说的话")
    ```

    注意：
      - 必须要有API访问密钥才能使用这个模型。
      - **kwargs 的参数将会传递给父类，具体取决于父类如何处理这些参数。
    """

    def __init__(self, apitoken=None, proxy=None, config_file=None, **kwargs: Any):
        """
        初始化ChatGPT3类。

        此类是OpenAI_Complete_Model的子类，用于创建ChatGPT3对象。

        ChatGPT3类实例化后，将创建一个与GPT-3.5-turbo模型的连接。

        参数：
            apitoken(str): OpenAI API的令牌。
            kwargs(dict, optional): 可选参数，用于控制模型的具体行为。可能包含例如temperature、max_tokens等参数。

        返回：
            None

        例子：
            >>> chatgpt = ChatGPT3(apitoken="your_api_token")
            >>> response = chatgpt.generate(prompt="Hello, world!")

        注意：
        此类需要有效的OpenAI API令牌才能使用。
        """

        super().__init__(model_name="gpt-3.5-turbo", apitoken=apitoken, price=(0.0015, 0.002),
                         config_file=config_file,
                         proxy=proxy, **kwargs)


class FineTuned_Completion_Model(OpenAI_Complete_Model):
    """
    这是一个细调完成模型类，它继承自OpenAI_Complete_Model类。

    细调完成模型类主要用于自定义OpenAI的模型参数。它的构造函数需要两个参数：模型ID和API令牌。在初始化时，它将模型的ID和API令牌传递给超类，同时设置模型的温度范围为0.03到0.06。

    使用示例：
    ```
    model = FineTuned_Completion_Model('text-davinci-002', 'my-api-token')
    ```

    参数:
    - model_id: 一个字符串，表示OpenAI模型的ID
    - apitoken: 一个字符串，表示API的令牌
    - **kwargs: 任意数量的关键字参数

    注意：尽管这个类已经设置了模型的温度范围，但是你仍然可以通过传入关键字参数来自定义设置。

    注意：这个类没有明显的错误或bug，但是在使用时需要注意API的令牌安全。

    请确保你的API令牌是正确且安全的，否则可能会导致无法访问模型的错误。
    """

    def __init__(self, model_id, apitoken=None, proxy=None, config_file=None, **kwargs: Any):
        """
        这是FineTuned_Completion_Model类的构造函数, 这个类是OpenAI_Complete_Model的子类, 用于实现微调模型的功能。

        参数:
            model_id: 用于微调的模型的ID
            apitoken: 连接OpenAI API的令牌
            **kwargs: 任意数量的关键字参数, 这些参数将传递给父类的构造函数。

        返回:
            无返回值

        使用示例:
            model = FineTuned_Completion_Model(model_id="text-davinci-001", apitoken="my-token", temperature=0.5)

        注意:
            我们在这里假设OpenAI_Complete_Model类的构造函数接受模型ID、API令牌和一个浮点数元组作为参数，如果实际情况并非如此，请根据实际情况进行修改。
        """

        super().__init__(model_name=model_id, apitoken=apitoken, price=(0.03, 0.06),
                         config_file=config_file,
                         proxy=proxy, **kwargs)
