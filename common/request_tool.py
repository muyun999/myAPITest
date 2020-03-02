import requests
import hashlib
from common import read_config
from pathlib import Path
from common.log_trace import mylog

readconfig = read_config.ReadConfig()


class CommonHttp:

    def __init__(self):
        global scheme, host, port, timeout
        scheme = readconfig.get_http("scheme")
        host = readconfig.get_http("baseurl")
        port = readconfig.get_http("port")
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
        filepath = pro_dir+f"\excle_data\{file}"
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

    def get_token(self):
        login_url = readconfig.get_login("login_url")
        login_username = readconfig.get_login("login_username")
        login_pw = readconfig.get_login("login_pw")
        # 密码转成hash密码
        login_pw_hash = hashlib.md5(bytes(login_pw, encoding="utf-8")).hexdigest()
        response = requests.post(url=login_url, data={"password": login_pw_hash, "username": login_username})
        login_token = response.json()["data"]["token"]
        if login_token:
            mylog().info("获取token成功")
            return response.json()["data"]["token"]
        else:
            mylog().info("获取token失败")

    def set_token(self):
        readconfig.cf.set("HEADERS", "token", self.get_token())
        with open(readconfig.config_path, "w+", encoding="utf-8") as f:
            readconfig.cf.write(f)


if __name__ == "__main__":
    a = CommonHttp()
    print(a.set_token())
