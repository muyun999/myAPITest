import configparser
from pathlib import Path

# 取当前文件的上上级路径
# pro_dir = os.path.split(os.path.realpath(__file__))[0]
pro_dir = Path(__file__).parents[1]
# 得到配置文件的路径
# config_path = os.path.join(pro_dir, 'config.ini')
# config_path = Path.joinpath(pro_dir, "config/config.ini")


class ReadConfig:
    def __init__(self):
        self.config_path = Path.joinpath(pro_dir, "config/config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(self.config_path, encoding='utf-8')

    def get_config(self, title, name):
        return self.cf.get(title, name)

    def get_http(self, name):
        return self.cf.get('HTTP', name)

    def get_email(self, name):
        return self.cf.get('EMAIL', name)

    def get_headers(self, name):
        return self.cf.get('HEADERS', name)

    def get_reportform(self, name):
        return self.cf.get('TESTREPORT', name)

    def get_login(self, name):
        return self.cf.get('LOGIN', name)

    def get_redis(self, name):
        return self.cf.get('REDIS', name)

    def get_db(self, name):
        return self.cf.get('MYSQL', name)

    def get_inidata(self, title, name):
        return self.cf.get(title, name)


if __name__ == '__main__':
    # a = ReadConfig().get_config('HTTP', 'port')
    print(Path(__file__).parents)


