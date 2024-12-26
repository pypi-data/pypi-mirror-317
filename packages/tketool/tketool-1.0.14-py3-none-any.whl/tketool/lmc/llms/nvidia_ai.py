from tketool.lmc.llms.openai import OpenAI_Complete_Model, Any


class NvidiaOpenSourceModel(OpenAI_Complete_Model):
    def __init__(self, model_name=None, price=None, apitoken=None, proxy=None, base_url=None, config_file=None, **kwargs: Any):
        super().__init__(model_name=model_name, price=price, apitoken=apitoken, proxy=proxy, base_url=base_url,
                         config_file=config_file, **kwargs)

    def parse_config_obj(self, base_url):
        self.proxy = self.config_obj.get_config("openai_proxy", "not_set")
        self.api_token = self.config_obj.get_config("nvidia_api_key", "not_set")
        self.base_url = self.config_obj.get_config('nvidia_base_url', 'not_set')
        self.model_name = self.config_obj.get_config('nvidia_model_name', 'not_set')


class Nvidia_LLama_3_70B(NvidiaOpenSourceModel):
    def __init__(self, apitoken=None, proxy=None, config_file=None, **kwargs: Any):
        super().__init__(model_name="'meta/llama3-70b-instruct'",
                         price=(0, 0),
                         apitoken=apitoken,
                         proxy=proxy,
                         base_url="https://integrate.api.nvidia.com/v1",
                         config_file=config_file,
                         **kwargs)
