# pass_generate
from tketool.JConfig import get_config_instance
from tketool.lmc.models import *
from tketool.lmc.llms.openai import *
from tketool.lmc.llms.zhipu_ai import *
# from langchain.chat_models import ChatOpenAI
import os
from tketool.lmc.llms.openai import OpenAI_Complete_Model
from typing import Optional, List, Dict, Mapping, Any


def get_init_llm():
    """
    这个函数的主要功能是初始化llm模型。它首先从Service_Shelve类实例中获取配置，提取出llm模型的类型，然后根据llm模型的类型分别初始化对应的模型。目前支持的模型类型有"gpt4"和"glm"。
    
    参数:
    无
    
    返回:
    返回初始化后的llm模型实例。
    
    错误处理:
    如果配置中的llm模型类型不在支持的类型列表中（"gpt4", "glm"），则会抛出异常。
    
    示例:
    
    ```python
    llm = get_init_llm()
    ```
    
    注意：
    在使用这个函数之前，需要确保已经正确配置了llm模型的类型。
    
    """

    config = get_config_instance()
    llm_type = config.get_config("llm_type", "chatgpt")

    if llm_type == "local":
        local_addr = config.get_config("local_model_ipaddr", "noset")
        local_model_name = config.get_config("local_model_name", "noset")
        local_model_token = config.get_config("local_model_token", "EMPTY")
        return OpenAI_Complete_Model(local_model_name, (0.01, 0.01), apitoken=local_model_token,
                                     base_url=local_addr)

    if llm_type == "gpt4":
        return Openai_ChatGPT_4_Turbo(config_file=config)
        # return OpenAI(temperature=float(temperature), model_name=model_name)

    if llm_type == "glm":
        return ChatGLM_local(config_file=config)

    raise Exception("Notset")
