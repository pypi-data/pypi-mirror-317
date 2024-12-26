# pass_generate
from typing import Any, List

from tketool.lmc.models import Emb_Plus
from langchain_openai import OpenAIEmbeddings
import requests, openai


class Openai_embedding(Emb_Plus):
    """
    Openai_embedding是一个继承自Emb_Plus的类，用于获取OpenAI的词嵌入。这个类需要通过使用OpenAI提供的API令牌才能工作，并且可以通过代理服务器进行网络连接。这个类的主要功能是将文本列表嵌入到浮点数列表中。
    
    类的使用方法如下:
    1. 实例化类时，需要提供OpenAI的API令牌
    2. 如果需要通过代理服务器进行网络连接，还需要提供代理信息
    3. 使用embed_str_list方法，可以将文本列表嵌入到浮点数列表中
    
    例子：
    ```python
    openai_emb = Openai_embedding(apitoken="your_openai_api_token")
    texts = ["Hello world", "I love python"]
    embeddings = openai_emb.embed_str_list(texts)
    ```
    
    参数：
    - `texts`：需要嵌入的文本列表，类型为列表，列表的元素是字符串
    - `apitoken`：OpenAI的API令牌，类型为字符串
    - `proxy`：代理服务器信息，类型为字符串，格式为"ip:port"，默认为None
    - `**kwargs`：其他参数，可以是任何类型
    
    返回：
    - `embed_str_list`方法，返回一个列表，列表的元素是浮点数列表，其中每个浮点数列表代表一个文本的嵌入
    
    注意：
    - 在使用该类时，需要确保你有一个有效的OpenAI API令牌，并且该令牌有权限访问OpenAI的词嵌入功能
    - 在使用代理服务器时，需要确保代理服务器可以正常访问OpenAI的服务器
    """

    def embed_str_list(self, texts: List[str], **kwargs: Any) -> List[List[float]]:
        """
        这个方法的主要用途是将一系列的文本通过OpenAI的词嵌入模型进行编码。
        
        Args:
            texts (List[str]): 这是一个字符串列表，每个元素是一个独立的文本，需要进行词嵌入编码的文本。
            **kwargs: 可变长度的关键字参数，用于接收未知数量的关键字参数。
        
        Returns:
            List[List[float]]: 返回的是一个嵌套列表，外层列表的每个元素对应输入的每个文本，内层列表则包含了该文本通过词嵌入模型编码后得到的浮点数值。
        
        示例：
            假设我们有一个文本列表`texts = ["hello", "world"]`，我们可以这样使用这个方法：
            ```python
            emb = Openai_embedding(apitoken="your_api_token")
            embeddings = emb.embed_str_list(texts)
            ```
            `embeddings`将会是一个包含两个子列表的列表，每个子列表都是一个浮点数的列表，这代表了"hello"和"world"这两个文本的词嵌入表示。
        """

        return self.emb_obj.embed_documents(texts)

    def __init__(self, apitoken=None, proxy=None, config_file=None, **kwargs):
        """
        这是一个初始化 Openai_embedding 类的构造函数。
        
        该函数主要用于初始化 Openai_embedding 类的实例对象。其中，Openai_embedding 类继承自 Emb_Plus 类，主要用于处理和管理 OpenAI 的嵌入向量。
        
        参数:
            apitoken (str): 用于访问 OpenAI API 的密钥。
            **kwargs: 用于 Emb_Plus 类的其他关键字参数。
        
        示例:
            >>> embedding = Openai_embedding(apitoken="your_openai_api_token")
            >>> text = "This is a test sentence."
            >>> vector = embedding.embed_str_list([text])
        """

        super().__init__("openai_embedding", config_file_path=config_file, **kwargs)

        if self.config_obj:
            self.proxy = self.config_obj.get_config("openai_proxy", "not_set")
            self.api_token = self.config_obj.get_config("openai_token", "not_set")
        else:
            self.api_token = apitoken
            self.proxy = proxy

        openai.api_key = self.api_token

        if self.proxy is not None:
            # os.environ['OPENAI_API_PROXY'] = ""
            openai.proxy = self.proxy  # "192.168.2.1:9999"

        self.emb_obj = OpenAIEmbeddings(openai_api_key=self.api_token)
