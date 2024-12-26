# # pass_generate
# from tketool.JConfig import get_config_instance
# from tketool.mlsample.LocalSampleSource import LocalDisk_NLSampleSource
# from tketool.lmc.llms import *
# from tketool.lmc.embeddings import *
#
#
# class Service_Shelve:
#     """
#     这个类`Service_Shelve`是一个配置管理类，它主要用于获取指定配置文件中的各种设置，如数据源路径、模型URL、API令牌等。
#     它通过读取配置文件，将配置内容实例化为config对象，并提供获取各种资源（如数据源、模型等）的方法。
#
#         示例:
#         ```
#         service_shelve = Service_Shelve("config_file_path")
#         datasource = service_shelve.get_datasource()
#         model = service_shelve.get_llm_GLM6B()
#         ```
#
#     方法列表：
#     - `__init__(self, config_file_path)`: 构造函数，接收一个config_file_path，这个路径是配置文件的路径。该函数将配置文件实例化为config对象。
#
#     - `get_config(self)`: 返回config对象。
#
#     - `get_datasource(self)`: 从配置文件中获取sample_source_path，然后根据路径实例化一个LocalDisk_NLSampleSource对象。
#
#     - `get_llm_GLM6B(self, buffer_version=-1)`: 从配置文件中获取glm_url配置，并将其实例化为ChatGLM对象。
#
#     - `get_llm_GPT4(self, buffer_version=-1)`: 从配置文件中获取openai_proxy、openai_token、openai_temperature配置，并将相关配置实例化为ChatGPT4对象。
#
#     - `get_llm_GPT35(self, buffer_version=-1)`: 从配置文件中获取openai_proxy、openai_token、openai_temperature配置，并将相关配置实例化为ChatGPT3对象。
#
#     - `get_ft_model(self, model_id, buffer_version=-1, **kwargs)`: 从配置文件中获取openai_proxy、openai_token、openai_temperature配置，并将相关配置与提供的model_id、**kwargs实例化为FineTuned_Completion_Model对象。
#
#     - `get_emb(self, buffer_version=-1, **kwargs)`: 从配置文件中获取openai_token、openai_proxy配置，并将相关配置实例化为Openai_embedding对象。
#     """
#
#     def __init__(self, config_file_path):
#         """
#         初始化Service_Shelve类。
#
#         这个类是一个服务存储器，负责管理和提供各种服务。这些服务可能包括数据源、多种语言模型、嵌入模型等。Service_Shelve通过读取一个配置文件来获取这些服务的配置信息，根据这些配置信息初始化相应的服务。
#
#         参数:
#             config_file_path (str): 配置文件的路径。这个配置文件中包含了各种服务的配置信息。
#
#         属性:
#             config_obj: 根据给定的配置文件路径生成的配置对象。这个配置对象之后会被用来获取各种服务的配置信息。
#
#         示例:
#
#             service_shelve = Service_Shelve("path/to/config/file")
#             glm6b_service = service_shelve.get_llm_GLM6B()
#             gpt4_service = service_shelve.get_llm_GPT4()
#             emb_service = service_shelve.get_emb()
#         """
#
#         self.config_obj = get_config_instance(config_file_path)
#
#     def get_config(self):
#         """
#         获取配置对象。
#
#         此方法是类Service_Shelve的一个方法，用于获取一个保存了某配置文件信息的对象。该对象可根据需要获取配置文件中的指定信息。
#
#         返回:
#             obj: 一个配置文件对象。可以根据需求获取配置文件中的指定信息。
#
#         示例:
#             service_shelve = Service_Shelve(config_file_path="config/path")
#             config_obj = service_shelve.get_config()
#         """
#
#         return self.config_obj
#
#     def get_datasource(self):
#         """
#         该函数用于获取数据源。
#
#         获取数据源的具体方式是通过配置文件（由self.config_obj所代表）来获取sample_source_path的值，该值代表数据源在本地磁盘的存储路径。然后，使用LocalDisk_NLSampleSource类来实例化一个数据源对象，该对象的特点是从本地磁盘读取样本来源。
#
#         函数没有参数。
#
#         返回类型是LocalDisk_NLSampleSource类的一个实例，代表一个可以从本地磁盘读取样本来源的数据源对象。
#
#         使用示例：
#         service_shelve = Service_Shelve(config_file_path)
#         datasource = service_shelve.get_datasource()
#
#         注意：如果配置文件中没有sample_source_path的配置项，或者该配置项的值不是一个有效的本地磁盘路径，可能会在运行时抛出异常。
#         """
#
#         data_folder_path = self.config_obj.get_config("sample_source_path")
#         return LocalDisk_NLSampleSource(data_folder_path)
#
#     def get_llm_GLM6B(self, buffer_version=-1):
#         """
#         此函数的目的是从配置文件获取GLM模型的URL，并返回GLM模型实例。
#
#         参数:
#             buffer_version(int, 可选): 版本号，默认为-1。
#
#         返回:
#             返回ChatGLM类的实例，这是一个机器学习模型。
#
#         例子:
#             service_shelve = Service_Shelve('config_file_path')
#             glm_model = service_shelve.get_llm_GLM6B()
#
#         注意:
#             需要先确保配置文件中存在"glm_url"这个配置项，并且其值是GLM模型的URL。
#         """
#
#         glm_url = self.config_obj.get_config("glm_url", "not_set")
#         return ChatGLM(glm_url, version=buffer_version)
#
#     def get_llm_GPT4(self, buffer_version=-1):
#         """
#         这个方法用于获取`ChatGPT4`模型实例。
#
#         参数:
#             buffer_version (int, optional): 版本号，默认是-1。
#
#         返回:
#             ChatGPT4: 返回带有指定参数的ChatGPT4实例。
#
#         解释:
#             该方法从配置对象中获取所需的配置信息（如代理设置、API令牌和温度参数）。然后，它使用这些配置信息创建一个新的ChatGPT4实例，并返回。
#
#             在函数内部，首先通过调用`self.config_obj.get_config`方法获取必要的配置，比如"openai_proxy"、"openai_token"和"openai_temperature"。
#
#             然后，将获取的temperature转换为float类型，并设置到配置字典config_dict中。
#
#             最后，使用获取到的api_token、proxys、config_dict和buffer_version作为参数，创建一个新的ChatGPT4对象，并返回。
#
#             例如：
#
#             ```python
#             service_shelve = Service_Shelve(config_file_path)
#             gpt4 = service_shelve.get_llm_GPT4(buffer_version=0)
#             ```
#
#         注意:
#             如果配置文件中没有设置相关的配置信息，"openai_proxy"和"openai_token"将默认为"not_set"，"openai_temperature"将默认为"0.8"。
#         """
#
#         proxys = self.config_obj.get_config("openai_proxy", "not_set")
#         api_token = self.config_obj.get_config("openai_token", "not_set")
#         temperature = self.config_obj.get_config("openai_temperature", "0.8")
#
#         config_dict = {'temperature': float(temperature)}
#
#         return ChatGPT4(api_token, proxy=proxys, call_dict=config_dict, version=buffer_version)
#
#     def get_llm_GPT35(self, buffer_version=-1):
#         """
#         此函数的目的是获取GPT-3.5语言模型的实例。
#
#         参数:
#         buffer_version (int, 默认值为-1): 指定的缓存版本，如果没有指定，则默认为-1。
#
#         返回:
#         返回的是一个ChatGPT3实例。该实例是使用从配置对象中获取的代理和API令牌创建的，温度参数也从配置对象中获取。
#
#         使用示例：
#         service_shelve = Service_Shelve(config_file_path)
#         gpt3_5_llm = service_shelve.get_llm_GPT35(buffer_version=1)
#
#         注意事项：
#         1. 这个函数从配置对象中获取了openai代理、openai令牌和openai温度这些配置。所以，应确保在调用此函数之前已经正确设置了这些配置。
#         2. 如果在创建ChatGPT3实例时发生错误，此函数不会捕获和处理这些错误，所以你需要自行处理可能出现的异常。
#         """
#
#         proxys = self.config_obj.get_config("openai_proxy", "not_set")
#         api_token = self.config_obj.get_config("openai_token", "not_set")
#         temperature = self.config_obj.get_config("openai_temperature", "0.8")
#
#         config_dict = {'temperature': float(temperature)}
#
#         return ChatGPT3(api_token, proxy=proxys, call_dict=config_dict, version=buffer_version)
#
#     def get_ft_model(self, model_id, buffer_version=-1, **kwargs):
#         """
#         此函数的主要目的是根据指定的模型ID和其他参数，获取一个经过微调的模型。
#
#         参数：
#             model_id (str) : 模型ID。
#             buffer_version (int, 可选) : 缓冲区版本，默认为 -1。
#             **kwargs : 其他一些需要传递给模型的参数。
#
#         返回：
#             FineTuned_Completion_Model 对象：一个经过微调的模型对象。
#
#         示例：
#             >>> service = Service_Shelve(config_file_path)
#             >>> ft_model = service.get_ft_model('gpt-3.5-turbo')
#             >>> result = ft_model.predict('Hello, how are you?')
#
#         注意：
#             - 在使用这个函数时，需要保证已经配置了openai代理和openai的api token，以及openai的温度参数，否则可能无法正确获取模型。
#             - 如果传递给此函数的buffer_version参数为负数，则会自动使用默认的buffer_version。
#             - 如果函数无法获取指定的模型ID，则可能会抛出异常。
#
#         错误：
#             - 如果获取的模型不存在或无法访问，将抛出异常。
#
#         """
#
#         proxys = self.config_obj.get_config("openai_proxy", "not_set")
#         api_token = self.config_obj.get_config("openai_token", "not_set")
#         temperature = self.config_obj.get_config("openai_temperature", "0.8")
#
#         config_dict = {'temperature': float(temperature), **kwargs}
#
#         return FineTuned_Completion_Model(model_id, api_token, proxy=proxys, call_dict=config_dict,
#                                           version=buffer_version)
#
#     def get_emb(self, buffer_version=-1, **kwargs):
#         """
#             get_emb是Service_Shelve类的一个方法，用于获取嵌入模型。
#
#             参数:
#             buffer_version(int, 可选): 缓冲区版本，默认为-1，表示使用最新版本。
#             **kwargs(dict, 可选): 允许用户提供额外的配置参数。
#
#             返回:
#             返回值是一个Openai_embedding实例。此实例可用于获取特定文本的嵌入表示。
#
#             举例:
#             ```python
#             service_shelve = Service_Shelve(config_file_path="config.json")
#             emb_model = service_shelve.get_emb()
#             text_embedding = emb_model.get_embedding("This is a test sentence")
#             ```
#
#             注意:
#             为了使用此函数，需要在配置文件中提供有效的OpenAI API令牌和代理服务器详细信息(如果使用)。如果这些信息未正确配置，函数可能会引发异常。
#
#             错误与异常:
#             如果给定的buffer_version无效，或者OpenAI API令牌或代理服务器详细信息未正确配置，此函数可能会引发异常。
#
#         """
#
#         api_token = self.config_obj.get_config("openai_token", "not_set")
#         proxys = self.config_obj.get_config("openai_proxy", "not_set")
#         return Openai_embedding(api_token, proxy=proxys, version=buffer_version)
