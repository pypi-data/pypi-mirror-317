import json
from tketool.lmc.models import LLM_Plus
from tketool.logs import log
from typing import Optional, List, Any


class XunFeiSparkModel(LLM_Plus):
    client: Optional[Any] = None
    ChatMessage: Optional[Any] = None
    ssl: Optional[Any] = None
    websocket: Optional[Any] = None
    thread: Optional[Any] = None
    app_id: Optional[str] = None
    app_secret: Optional[str] = None
    app_key: Optional[str] = None
    app_url: Optional[str] = None
    stream_answer: Optional[str] = None
    spark_model: Optional[str] = None
    call_model_invoker: Optional[Any] = None

    def __init__(self, spark_app_id, spark_app_secret, spark_app_key, spark_app_url, spark_model_name, spark_price,
                 call_method='sdk', config_file=None, **kwargs: Any):

        """
        调用讯飞星火大模型
        参数：
        - spark_app_id, spark_app_secret, spark_app_key: 模型调用身份验证凭证，str, 获取方式：https://www.xfyun.cn/doc/spark/general_url_authentication.html
        - spark_app_url： 模型获取url地址，str
        - spark_model_name: 星火模型名称
        - spark_price：星火模型调用价格，元组 （输入价格，输出价格）
        - call_method： 模型调用方式，str, 可选api、sdk, 默认为sdk
        - config_file: config文件路径
        """

        super().__init__(model_name=spark_model_name, price=spark_price, config_file_path=config_file, **kwargs)

        if not spark_app_id and not config_file:
            log('Spark params must be given by config file or Parameter passing')

        if not spark_app_id and config_file:
            spark_app_id = self.config_obj.get_config('xunfei_app_id', 'not_set')
            spark_app_secret = self.config_obj.get_config('xunfei_app_secret', 'not_set')
            spark_app_key = self.config_obj.get_config('xunfei_app_key', 'not_set')
            spark_app_url = self.config_obj.get_config('xunfei_app_url', r'wss://spark-api.xf-yun.com/v3.5/chat')
            spark_model_name = self.config_obj.get_config('xunfei_model_name', 'generalv3.5')

        self.call_method_select(call_method, spark_app_url, spark_app_id, spark_app_key, spark_app_secret, spark_model_name)

    def call_method_select(self, call_method, spark_app_url, spark_app_id, spark_app_key, spark_app_secret, spark_model):
        match call_method:
            case 'sdk':
                try:
                    from sparkai.llm.llm import ChatSparkLLM, ChatMessage

                    self.client = ChatSparkLLM(
                        spark_api_url=spark_app_url,
                        spark_app_id=spark_app_id,
                        spark_api_key=spark_app_key,
                        spark_api_secret=spark_app_secret,
                        spark_llm_domain=spark_model,
                        **self.call_dictionary_config
                    )
                    self.ChatMessage = ChatMessage
                except ImportError as e:
                    raise Exception("Unable to import ChatSparkLLM from sparkai, please install: spark_ai_python")

                self.call_model_invoker = self.call_model_sdk

            case 'api':
                self.app_id = spark_app_id
                self.app_secret = spark_app_secret
                self.app_key = spark_app_key
                self.spark_model = spark_model
                self.app_url = spark_app_url
                self.stream_answer = ''

                try:
                    import ssl
                    import websocket
                    import _thread as thread

                    self.ssl = ssl
                    self.websocket = websocket
                    self.thread = thread

                except ImportError as e:
                    raise Exception(e)

                self.call_model_invoker = self.call_model_api

            case _:
                raise Exception(f"call method must be sdk or api, but '{call_method}'")

    def _construct_query(self, prompt: str) -> List:
        messages = [self.ChatMessage(
            role='user',
            content=prompt
        )]

        return messages

    def _invoke_model(self, prompt):
        response = self.client.generate([prompt])

        return response

    def _parse_invoke_result(self, response):
        answer = response.generations[0][0].text
        tokens_cost = response.llm_output['token_usage']
        prompt_token_count = tokens_cost["prompt_tokens"]
        completion_token_count = tokens_cost["completion_tokens"]

        cost = self.calculate_cost(prompt_token_count, completion_token_count)

        return answer, cost

    def call_model_sdk(self, prompt, return_detail, *args, **kwargs) -> Any:
        query = self._construct_query(prompt)
        invoke_result = self._invoke_model(query)
        result, cost = self._parse_invoke_result(invoke_result)

        if return_detail:
            return result, cost

        return result

    def gen_params(self, query):
        """
        通过appid和用户的提问来生成请参数
        """

        data = {
            "header": {
                "app_id": self.app_id,
                "uid": "1234",
                # "patch_id": []    #接入微调模型，对应服务发布后的resourceid
            },
            "parameter": {
                "chat": {
                    "domain": self.model_name,
                    # "temperature": 0.5,
                    "max_tokens": 4096,
                    "auditing": "default",
                    **self.call_dictionary_config
                }
            },
            "payload": {
                "message": {
                    "text": [{"role": "user", "content": query}]
                }
            }
        }
        return data

    def call_model_api(self, prompt, return_detail, *args, **kwargs) -> Any:
        # 收到websocket错误的处理
        def on_error(ws, error):
            # log("\n### error:", error)
            pass

        # 收到websocket关闭的处理
        def on_close(ws, close_status_code, close_msg):
            pass

        # 收到websocket连接建立的处理
        def on_open(ws):
            self.thread.start_new_thread(run, (ws,))

        def run(ws, *args):
            data = json.dumps(self.gen_params(query=ws.query))
            ws.send(data)

        # 收到websocket消息的处理
        def on_message(ws, message):
            # print(message)
            data = json.loads(message)
            code = data['header']['code']
            if code != 0:
                # log(f'请求错误: {code}, {data}')
                self.stream_answer = ''
                ws.content = self.stream_answer
                ws.close()
            else:
                choices = data["payload"]["choices"]
                status = choices["status"]
                content = choices["text"][0]["content"]
                # print(content, end='')

                # 流式获取，需要拼接得到完整内容
                self.stream_answer = self.stream_answer + content

                if status == 2:
                    ws.content = self.stream_answer
                    ws.close()

                    prompt_token_count = data['payload']['usage']['text']['prompt_tokens']
                    completion_token_count = data['payload']['usage']['text']['completion_tokens']

                    cost = self.calculate_cost(prompt_token_count, completion_token_count)
                    # self.add_token_use((prompt_token_count, completion_token_count))

                    ws.cost = cost
                    self.stream_answer = ''

        ws_param = WebsocketParam(self.app_id, self.app_key, self.app_secret, self.app_url)
        self.websocket.enableTrace(False)
        ws_url = ws_param.create_url()

        ws = self.websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close,
                                         on_open=on_open)
        ws.appid = self.app_id
        ws.query = prompt
        ws.domain = self.spark_model
        ws.run_forever(sslopt={"cert_reqs": self.ssl.CERT_NONE})

        if return_detail:
            return ws.content, ws.cost

        return ws.content

    def call_model(self, prompt, return_detail, *args, **kwargs) -> Any:
        return self.call_model_invoker(prompt, return_detail, *args, **kwargs)


class WebsocketParam(object):
    # 初始化
    def __init__(self, app_id, api_key, api_secret, app_url):

        try:
            import base64
            import hashlib
            import hmac
            from time import mktime
            from datetime import datetime
            from urllib.parse import urlparse, urlencode
            from wsgiref.handlers import format_date_time

            self.format_date_time = format_date_time
            self.urlencode = urlencode
            self.base64 = base64
            self.hashlib = hashlib
            self.hmac = hmac
            self.datetime = datetime
            self.mktime = mktime

        except ImportError as e:
            raise Exception(e)

        self.APPID = app_id
        self.APIKey = api_key
        self.APISecret = api_secret
        self.host = urlparse(app_url).netloc
        self.path = urlparse(app_url).path
        self.gpt_url = app_url

    # 生成url
    def create_url(self):
        # 生成RFC1123格式的时间戳
        now = self.datetime.now()
        date = self.format_date_time(self.mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        # 进行hmac-sha256进行加密
        signature_sha = self.hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                      digestmod=self.hashlib.sha256).digest()

        signature_sha_base64 = self.base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'

        authorization = self.base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        # 拼接鉴权参数，生成url
        url = self.gpt_url + '?' + self.urlencode(v)

        return url


class XunFei_Spark_35(XunFeiSparkModel):
    def __init__(self, spark_app_id=None, spark_app_secret=None, spark_app_key=None, call_method='sdk', config_file=None, **kwargs: Any):
        super().__init__(spark_app_id,
                         spark_app_secret,
                         spark_app_key,
                         spark_app_url="wss://spark-api.xf-yun.com/v3.5/chat",
                         spark_model_name='generalv3.5',
                         spark_price=(0.03, 0.03),
                         call_method=call_method,
                         config_file=config_file, **kwargs)

