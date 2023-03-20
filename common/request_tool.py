import requests
from common import read_config
from pathlib import Path
from common.log_trace import mylog
import redis

readconfig = read_config.ReadConfig()


class CommonHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = readconfig.get_http("scheme")
        host = readconfig.get_http("baseurl")
        timeout = readconfig.get_http("timeout")

        self.data = {}
        self.headers = {}
        self.params = {}
        self.files = {}
        self.url = None

    def set_url(self, url=None):
        self.url = scheme+"://"+host + url if url else scheme+"://"+host
        return self.url

    def set_headers(self, headers):
        self.headers = headers

    def set_params(self, params):
        self.params = params

    def set_data(self, data):
        self.data = data

    def set_file(self, file):
        # 取项目绝对地址
        pro_dir = Path(__file__).parents[1]
        filepath = pro_dir+f"\excel_data\{file}"
        self.files = {file: open(filepath, "rb")}

    def get(self):
        response = requests.get(url=self.url, headers=self.headers, params=self.params, timeout=timeout)
        return response

    def post(self):
        response = requests.post(url=self.url, headers=self.headers, params=self.params, data=self.data, timeout=timeout)
        return response

    def post_withfile(self):
        response = requests.post(url=self.url, headers=self.headers, files=self.files, timeout=timeout)
        return response

    def send_request(self, method, url, **kwargs):
        response = requests.request(method, url, **kwargs)
        return response

    def get_token(self):
        ''' 从redis中获取token,为了跳过验证码的登录操作 '''
        redis_host = readconfig.get_redis("host")
        redis_port = readconfig.get_redis("port")
        redis_db = readconfig.get_redis("db")
        token_key = readconfig.get_redis("token_key")
        r = redis.from_url(url=f'redis://:@{redis_host}:{redis_port}/{redis_db}')
        _token_key = r.keys(token_key)
        if _token_key:
            token = r.hget(_token_key[0], "token")
            return token
        else:
            mylog().warn("token does not exist in redis,please login again")

    def set_token(self):
        readconfig.cf.set("HEADERS", "token", self.get_token())
        with open(readconfig.config_path, "w+", encoding="utf-8") as f:
            readconfig.cf.write(f)


if __name__ == "__main__":
    a = CommonHttp()
    print(a.set_token())
