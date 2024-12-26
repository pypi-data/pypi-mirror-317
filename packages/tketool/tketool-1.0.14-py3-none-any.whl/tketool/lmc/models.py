import abc
from pydantic import BaseModel
from datetime import datetime
from tketool.utils.LocalRedis import *
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.embeddings.base import Embeddings
from typing import Optional, List, Dict, Mapping, Any, Tuple
import requests, openai, os
from tketool.logs import log
from tketool.buffer.bufferbase import *
from threading import Lock
import threading


class LLM_Plus(LLM):
    """
    LLM_Plus是LLM的子类，主要目的是在LLM的基础上增加了一些自定义的功能，并对一些方法进行了重写或者添加。
    
    这个类主要有以下几个属性：
    
    - proxy: 代理地址，默认为空。
    
    - model_name: 模型的名称。
    
    - use_buffer: 是否使用缓存，默认为False。
    
    - buffer_version: 缓冲版本，默认为-1。
    
    - call_dictionary_config: 调用字典配置。
    
    - price: 价格，是一个元组，默认为(0.0, 0.0)。
    
    此外，LLM_Plus类还提供了以下几个方法：
    
    - `__init__(self, model_name, version=-1, call_dict={}, price=(0.0, 0.0), proxy=None, **kwargs: Any)`: 构造函数，初始化LLM_Plus类的实例。
    
    - `add_token_use(self, use: (int, int))`: 添加token使用。
    
    - `call_model(self, prompt, *args, **kwargs) -> Any`: 抽象方法，需要子类重写，用于调用模型。
    
    - `_call(self, *args: Any, **kwargs: Any) -> str`: 私有方法，用于调用模型，并处理缓冲的情况。
    
    - `_llm_type(self) -> str`: 属性方法，返回模型名称。
    
    使用示例：
    
    ```
    llm_plus = LLM_Plus('my_model', 1.0, {'key': 'value'}, (0.1, 0.2), 'http://my_proxy.com')
    llm_plus.add_token_use((10, 20))
    result = llm_plus._call('my_prompt')
    ```
    
    注意事项：
    
    - 如果想要使用缓存，需要将version参数设置为大于0的值。
    
    - `call_model`方法需要在子类中重写，否则会抛出`NotImplementedError`异常。
    
    - `add_token_use`方法在添加token使用时，会对使用量进行记录，并且会计算并记录使用的总成本。
    
    - `_call`方法在调用模型时，会先检查是否使用缓存，如果使用缓存且缓存中有对应的结果，则直接返回。否则，会调用`call_model`方法，并将结果存入缓存中。
    
    - 如果调用`_call`方法时传入的参数中包含`call_dictionary_config`中的键，则`call_dictionary_config`中的值会被覆盖。
    """

    model_name: Optional[str] = ""
    # buffer_version: Optional[float] = -1.0
    call_dictionary_config: Dict = {}
    price: Optional[Tuple] = (0.0, 0.0)
    config_obj: Optional[ConfigManager] = None
    detail_dict: Dict = {}

    def __init__(self, model_name, call_dict={}, price=(0.0, 0.0), config_file_path=None, **kwargs: Any):
        """
            初始化LLM_Plus类的实例。
        
            LLM_Plus类是LLM类的子类，主要在LLM类的基础上增加了价格、使用缓存和代理等属性，以及对相应属性的操作方法。
        
            使用示例：
            ```python
            llm_plus = LLM_Plus(model_name="example_model", version=1.0, call_dict={'key': 'value'}, price=(1.0, 2.0), proxy="http://127.0.0.1:8000")
            ```
        
            参数列表：
            model_name : str
                模型名称。
            version : int, 默认值为-1
                模型的版本号。如果版本号大于0，则启用缓存。
            call_dict : dict, 默认值为空字典
                调用模型时的参数字典。
            price : Tuple[float, float], 默认值为(0.0, 0.0)
                模型的价格，为一个包含两个浮点数的元组。
            proxy : str, 默认值为None
                代理服务器的地址。
            **kwargs : Any
                存放其他参数的字典。
        
            返回类型：
            无返回值。
        
            注意事项：
            1. 如果`model_name`为空或者`version`小于0，将不启用缓存。
            2. 当调用`call_model`方法时，需要确保`call_dict`中的参数正确，否则可能导致调用失败。
        
            错误与异常：
            1. 如果指定的代理服务器无法连接，将导致网络调用失败。
            2. 如果`price`不是一个包含两个浮点数的元组，将引发TypeError。
        
        """

        super().__init__(**kwargs)
        self.model_name = model_name
        # self.buffer_version = version
        self.call_dictionary_config = call_dict
        self.price = price

        if config_file_path:
            if isinstance(config_file_path, str):
                self.config_obj = get_config_instance(config_file_path)
            else:
                self.config_obj = config_file_path
        else:
            self.config_obj = None

    def calculate_cost(self, in_tok, out_tok):
        cost = {
            "input_token": in_tok,
            "output_token": out_tok,
            "input_cost": self.price[0] * in_tok / 1000,
            "output_cost": self.price[1] * out_tok / 1000,
            "total": self.price[0] * in_tok / 1000 + self.price[1] * out_tok / 1000,
            "model_name": self.model_name
        }
        self.set_last_detail(cost)
        return cost

    def set_last_detail(self, detail):
        current_thread = threading.current_thread()
        thread_id = current_thread.ident
        self.detail_dict[thread_id] = detail

    def get_last_detail(self):
        current_thread = threading.current_thread()
        thread_id = current_thread.ident
        if thread_id in self.detail_dict:
            return self.detail_dict[thread_id]
        return None

    # def add_token_use(self, use: (int, int)):
    #     """
    #     此方法用于在调用模型后添加token使用量。
    #
    #     参数:
    #         use: (int, int), 一个元组，其中包含两个整型值。其中第一个整型值表示输入的token使用量，第二个整型值表示输出的token使用量。
    #
    #     返回:
    #         无返回值。
    #
    #     此方法首先获取当前日期，并以此构建一个特定的键名。如果该键名在内存中不存在值，则为其设置初始值0。并且为输入的token使用量和输出的token使用量设置初始价格。
    #
    #     之后，此方法会更新输入和输出的token使用量，并计算当前的成本。最后，该方法将会记录这些信息。
    #
    #     注意：此方法不会返回任何值，其主要目的是记录模型使用的token量和相应的成本。
    #     """
    #
    #     now = datetime.now()
    #     date_time_str = now.strftime("%m_%d")
    #     keyname = f"lm_{date_time_str}_{self.model_name}"
    #
    #     if not has_value(keyname):
    #         set_value(keyname, 0)
    #         set_value(keyname + "_use_in", 0)
    #         set_value(keyname + "_use_out", 0)
    #         set_value(keyname + "_use_in_price", self.price[0])
    #         set_value(keyname + "_use_out_price", self.price[1])
    #
    #     value_add(keyname + "_use_in", use[0])
    #     value_add(keyname + "_use_out", use[1])
    #
    #     current_cost = get_value(keyname + '_use_in') / 1000 * self.price[0] + self.price[1] / 1000 * get_value(
    #         keyname + '_use_out')
    #
    #     log(f"{self.model_name} add token:{use[0]}/{use[1]}"
    #         f" totle {get_value(keyname + '_use_in')}/{get_value(keyname + '_use_out')} "
    #         f" cost {round(current_cost, 2)}"
    #         f"")

    @abc.abstractmethod
    def call_model(self, prompt, return_detail, *args, **kwargs) -> Any:
        """
        该函数是一个抽象方法，需要在子类中实现。它的主要作用是调用模型。
        
        参数:
            prompt: 主要用于模型的提示语。
            *args: 可变参数，可传入多个任意类型的参数。
            **kwargs: 可变参数，可传入多个关键字参数。
        
        返回类型:
            Any: 返回任意类型的数据。
        
        使用示例:
            在子类中重写此方法，例如：
        
            class MyModel(LLM_Plus):
                def call_model(self, prompt, *args, **kwargs):
                    # 在这里实现模型的调用
                    result = my_model.predict(prompt)
                    return result
        
            这样，当我们创建MyModel的实例并调用call_model方法时，就会调用我们定义的模型并返回预测结果。
        
        注意:
            由于这是一个抽象方法，所以在使用LLM_Plus类时，必须创建其子类并实现这个方法，否则将会引发TypeError。
        """

        pass

    def _call(self, *args: Any, return_detail=False, **kwargs: Any) -> str:
        """
            `_call`是一个私有方法，主要用于处理模型调用的请求。这个方法首先会检查是否使用缓存，如果使用并且缓存版本号与当前版本号相同，那么就会直接返回缓存的结果。如果不使用缓存或缓存版本号不同，那么就会重新构建关键字参数`kwargs`，并调用模型进行计算，然后返回计算结果。
        
            参数:
            - `*args: Any`: 可变参数，用于传递给模型调用的参数。
            - `**kwargs: Any`: 可变关键字参数，用于传递给模型调用的关键字参数。
        
            返回:
            - `str`: 模型调用的结果。
        
            示例:
            ```python
            _call('input_text', key1='value1', key2='value2')
            ```
        
            注意:
            此方法是私有方法，一般不应该在类的外部直接调用。同时，因为此方法依赖于`call_model`抽象方法，所以在使用此类时，必须先实现`call_model`方法。
            """

        # rebuild kwargs
        new_kwargs = {**kwargs, **self.call_dictionary_config}
        call_result = self.call_model(*args, return_detail=return_detail, **new_kwargs)
        return call_result

    @property
    def _llm_type(self) -> str:
        """
            这是一个属性装饰器函数，用于返回LLM_Plus对象的model_name属性的值。此函数没有参数，并且返回一个字符串类型的值。
        
            属性装饰器的功能是将一个方法变为只读的类属性，使其可以像访问属性一样调用方法，这个方法没有输入参数。
        
            返回:
                返回model_name属性的值，该值是一个字符串类型。
        """

        return self.model_name

    def __call__(self, *args, return_detail=False, **kwargs):
        invoke_result = self._call(return_detail=return_detail, *args, **kwargs)
        return invoke_result


class LLM_Buffer_Plus(LLM_Plus):
    base_llm: LLM_Plus = None
    buffer_version: int = -1

    def __init__(self, base_model: LLM_Plus, buffer_version=-1):
        super().__init__(base_model.model_name)
        self.base_llm = base_model
        self.buffer_version = buffer_version

    def call_model(self, prompt, return_detail, *args, **kwargs) -> Any:

        nkey = get_hash_key(self.model_name, prompt, args, kwargs)
        if has_item_key(nkey):
            # log_debug("use_buffer")
            buffer_value = get_buffer_item(nkey)
            if buffer_value['version'] == self.buffer_version:
                buffer_value['detail']['hit_buffer'] = True
                self.set_last_detail(buffer_value['detail'])
                if return_detail:
                    return buffer_value['value'], buffer_value['detail']
                else:
                    return buffer_value['value']

            # rebuild kwargs
        new_kwargs = {**kwargs, **self.call_dictionary_config}

        call_result, details = self.base_llm(prompt, *args, return_detail=True, **new_kwargs)
        self.set_last_detail(details)
        buffer_item(nkey, {'version': self.buffer_version, 'value': call_result, 'detail': details})
        flush()

        if return_detail:
            return call_result, details
        else:
            return call_result


class Emb_Plus(Embeddings):
    """
    `Emb_Plus`类是一个嵌入类，它继承了`Embeddings`类。这个类用于处理文本数据，将文本转化为向量。它的主要功能包括通过指定的模型名和版本来初始化嵌入对象，添加代币使用量，嵌入字符串列表，嵌入文档，以及嵌入查询。
    
    类变量：
    - proxy: 可选的代理设置，默认为空。
    - model_name: 可选的模型名称，默认为空。
    - use_buffer: 是否使用缓冲，默认为False。
    - buffer_version: 缓冲版本，默认为-1.0。
    - call_dictionary_config: 调用字典配置， 默认为空字典。
    - price: 嵌入的价格，默认为(0.0, 0.0)。
    
    方法：
    - `__init__`: 初始化方法，用于设定模型名称、版本、调用字典、价格和代理等。
    - `add_token_use`: 添加代币使用量，根据模型名和当前日期来生成密钥名称，并将使用量添加到相应的密钥。
    - `embed_str_list`: 抽象方法，需要在子类中实现。接受一个字符串列表，返回一个嵌入向量的列表。
    - `embed_documents`: 接受一个文本列表，返回一个嵌入向量的列表。如果启用了缓冲，会从缓冲中获取数据；否则，会调用`embed_str_list`方法进行嵌入。
    - `embed_query`: 接受一个查询文本，返回一个嵌入向量。
    
    使用例子：
    ```python
    embedder = Emb_Plus("model_name")
    embedder.add_token_use((1, 2))
    vector = embedder.embed_query("query text")
    ```
    """

    model_name: Optional[str] = ""
    use_buffer: bool = False
    buffer_version: Optional[float] = -1.0
    call_dictionary_config: Dict = {}
    price: Optional[Tuple] = (0.0, 0.0)
    config_obj: Optional[ConfigManager] = None

    def __init__(self, model_name, version=-1, call_dict={}, price=(0.0, 0.0), config_file_path=None, **kwargs: Any):
        """
        这是一个名为 Emb_Plus 的类，继承自 Embeddings 类。目的是实现特定的词嵌入功能。该类对父类进行了扩展，提供了额外的功能，如代理、价格、缓冲区版本、模型名称等。
        
        类初始化方法 __init__ 的功能是初始化 Emb_Plus 实例的各项参数。
        
        参数:
            model_name: str, 模型名称。用于标识用户所使用的模型。
            version: int, 默认为-1，表示缓冲版本号。当版本号大于0时，启用缓冲区。
            call_dict: dict, 默认为空字典，表示调用字典配置。可以自定义传入的参数。
            price: tuple, 默认为 (0.0, 0.0)，表示使用代币的价格，包括进入和出去的价格。
            proxy: str, 默认为 None，表示代理。如果需要使用代理则可以指定。
            **kwargs: Any, 表示可以接受任意数量的额外参数。
        
        返回:
            无
        
        示例:
            emb_plus = Emb_Plus(model_name='model1', version=1, call_dict={'key': 'value'}, price=(1.0, 0.5), proxy='http://127.0.0.1:8080')
            这个示例创建了一个 Emb_Plus 的实例，指定了模型名称、版本号、调用字典配置、价格和代理。
        """

        super().__init__(**kwargs)
        self.model_name = model_name
        self.use_buffer = True if version > 0 else False
        self.buffer_version = version
        self.call_dictionary_config = call_dict
        self.price = price

        if config_file_path:
            if isinstance(config_file_path, str):
                self.config_obj = get_config_instance(config_file_path)
            else:
                self.config_obj = config_file_path
        else:
            self.config_obj = None

    def add_token_use(self, use: (int, int)):
        """
        这个方法是`Emb_Plus`类的一部分，用于追踪和更新token的使用情况。
        
        具体来说，它取得一个包含输入与输出token数量的元组，然后根据当前日期和模型名称生成一个键名，用于存储token使用的统计数据。
        
        如果该键名在数据库中不存在，则会为该键创建初始值为0的数据。并且还会创建两个以"_use_in"和"_use_out"为后缀的键，用于跟踪输入和输出token的使用。
        
        然后，方法会更新"_use_in"和"_use_out"的值，增加输入和输出token的数量。
        
        最后，计算当前的成本，即每1000个输入token的价格加上每1000个输出token的价格，然后将计算结果写入日志中。
        
        参数:
            use: 一个元组，包含两个整数，分别表示输入和输出token的数量。
        
        返回类型:
            无
        """

        now = datetime.now()
        date_time_str = now.strftime("%m_%d")
        keyname = f"lm_{date_time_str}_{self.model_name}"

        if not has_value(keyname):
            set_value(keyname, 0)
            set_value(keyname + "_use_in", 0)
            set_value(keyname + "_use_out", 0)
            set_value(keyname + "_use_in_price", self.price[0])
            set_value(keyname + "_use_out_price", self.price[1])

        value_add(keyname + "_use_in", use[0])
        value_add(keyname + "_use_out", use[1])

        current_cost = get_value(keyname + '_use_in') / 1000 * self.price[0] + self.price[1] / 1000 * get_value(
            keyname + '_use_out')

        log(f"{self.model_name} add token:{use[0]}/{use[1]}"
            f" totle {get_value(keyname + '_use_in')}/{get_value(keyname + '_use_out')} "
            f" cost {round(current_cost, 2)}"
            f"")

    @abc.abstractmethod
    def embed_str_list(self, texts: List[str], **kwargs: Any) -> List[List[float]]:
        """
        此抽象方法用于嵌入字符串列表。
        
        参数:
            texts (List[str]): 要嵌入的字符串列表。
            **kwargs: 其他可选参数。
        
        返回:
            List[List[float]]: 返回嵌入后的二维浮点数列表。
        
        示例:
            假设我们有一个实现了embed_str_list方法的Emb_Plus子类实例em。
            texts = ["Hello World", "Machine Learning"]
            em.embed_str_list(texts)
        
        注意:
            这是一个抽象方法，需要在子类中实现。
        """

        pass

    def embed_documents(self, texts: List[str], **kwargs: Any) -> List[List[float]]:
        """
        该函数的目标是嵌入给定的文档列表，并返回嵌入的结果。
        
        参数:
        texts: 文档列表，每个文档是一个字符串。
        **kwargs: 这是一个额外的参数列表，这将被用来传递给embed_str_list方法，这是该类定义的一个抽象方法。
        
        返回:
        该函数返回一个列表，其中包含每个文档的嵌入结果。每个结果都是一个浮点数列表。
        
        在函数的实现中，首先检查是否启用了缓冲区。如果启用了缓冲区，它将首先尝试从缓冲区中获取嵌入结果。如果在缓冲区中找到匹配项，并且其版本与当前的buffer_version匹配，那么将直接返回缓冲区中的值。
        
        如果没有启用缓冲区，或者在缓冲区中没有找到匹配的项或版本不匹配，那么它将调用embed_str_list方法，使用texts和kwargs作为参数来获取嵌入结果。
        
        在得到嵌入结果后，如果启用了缓冲区，它将将嵌入结果及其版本添加到缓冲区中，并立即刷新缓冲区。
        
        最后，返回嵌入结果。
        """

        if self.use_buffer:
            nkey = get_hash_key(self.model_name, texts)
            if has_item_key(nkey):
                # log_debug("use_buffer")
                buffer_value = get_buffer_item(nkey)
                if buffer_value['version'] == self.buffer_version:
                    return buffer_value['value']

        # rebuild kwargs
        new_kwargs = {**kwargs, **self.call_dictionary_config}

        call_result = self.embed_str_list(texts, **new_kwargs)
        if self.use_buffer:
            buffer_item(nkey, {'version': self.buffer_version, 'value': call_result})
            flush()

        return call_result

    def embed_query(self, text: str) -> List[float]:
        """
        该方法是将输入的文本进行向量化处理。
        
        参数:
            text (str): 需要进行向量化处理的输入文本。
        
        返回:
            List[float]: 返回处理后的向量，它是一个浮点数列表。
        
        使用示例:
            embed = Emb_Plus(...)
            vector = embed.embed_query("需要转化的文本")
            print(vector)
        
        注意：
            Output的维度取决于模型的类型和配置。例如，如果使用的是BERT模型，那么每个词的向量维度可能为768或1024等。
        
        方法的主要步骤：
            1. 输入文本被封装为一个列表，即[text]，然后传递给self.embed_documents方法进行处理。
            2. embed_documents方法返回的结果是一个列表的列表（即二维列表），这是因为它设计为处理多个文本输入。
            3. 但是embed_query只处理一个文本输入，所以它仅返回embed_documents返回的二维列表中的第一个元素（即一个一维向量）。
        
        此外，如果已经缓存了text的向量化结果，并且缓存的版本和当前版本一致，embed_documents方法会直接返回缓存的结果，提高处理效率。
        """

        return self.embed_documents([text])[0]
