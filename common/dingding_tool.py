import requests
import json
from common.log_trace import *

readconfig = read_config.ReadConfig()


def dingding_content():
    webhook = readconfig.get_inidata("DINGDING", "webhook")
    # allure地址
    allure_url = ""
    msg = "".join(log_analyse())+"\nallure报告链接\n"+allure_url
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {'msgtype': 'text', 'text': {'content': msg}, 'at': {'atMobiles': [], 'isAtAll': False}}
    #@接受钉钉消息人
    # at_people = {}
    # data['at']['atMobiles'].extend([at_people[module] for module in at_people.keys() if module in msg])
    post_data = json.dumps(data)
    response = requests.post(webhook, headers=headers, data=post_data)
    return response.text


def send_dingding():
    # 判断邮件发送开关
    on_off = readconfig.get_inidata("DINGDING", "on_off")
    if on_off == "on":
        try:
            dingding_content()
        except Exception as ex:
            mylog().error(str(ex))
        finally:
            mylog().info("钉钉消息已发送")

    elif on_off == 'off':
        mylog().info("钉钉开关为off,不发送钉钉消息")
    else:
        mylog().info("请检查钉钉开关配置")


