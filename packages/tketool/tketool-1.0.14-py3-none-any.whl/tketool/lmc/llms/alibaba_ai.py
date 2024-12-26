from tketool.lmc.llms.openai import OpenAI_Complete_Model, Any


class AlibabaQwen(OpenAI_Complete_Model):
    """
    # 阿里千问调用，参考链接：https://help.aliyun.com/zh/dashscope/developer-reference/?spm=a2c4g.11186623.0.0.18fd7defUsA7E4
    """
    def __init__(self, model_name, price, apitoken=None, proxy=None,
                 base_url=None, config_file=None, **kwargs: Any):
        super().__init__(model_name=model_name, price=price, apitoken=apitoken, proxy=proxy, base_url=base_url,
                         config_file=config_file, **kwargs)

    def parse_config_obj(self, base_url):
        self.proxy = None
        self.api_token = self.config_obj.get_config("alibaba_api_key", "not_set")
        self.base_url = self.config_obj.get_config('alibaba_base_url', 'not_set')
        self.model_name = self.config_obj.get_config('alibaba_model_name', 'not_set')


class Alibaba_Qwen_Plus(AlibabaQwen):
    def __init__(self, apitoken=None, config_file=None, **kwargs: Any):
        super().__init__(model_name='qwen-plus',
                         price=(0.02, 0.02),
                         apitoken=apitoken,
                         proxy=None,
                         base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
                         config_file=config_file,
                         **kwargs)