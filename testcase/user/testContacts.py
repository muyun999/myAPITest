import unittest
import parameterized
import requests
from common.excle_tool import get_title, get_param
from common.read_config import ReadConfig

localReadConfig = ReadConfig()


# 货主工作台地址管理查询接口
def get_contacts(paramslist):
    excle_titlelist = get_title("getContacts", "预期result")
    excle_datalist = list(paramslist)
    url = "http://workbench.optima-trans.net/v1/user/contacts"
    headers = {"token": str(localReadConfig.get_headers("token"))}
    res = requests.get(url=url, headers=headers, params=dict(zip(excle_titlelist, excle_datalist)))
    result = str(res.json().get("data").get("total"))
    return result


# 货主工作台地址管理新增地址接口
def add_contacts(paramslist):
    excle_titlelist = get_title("addContacts")
    excle_datalist = list(paramslist)
    url = "http://workbench.optima-trans.net/v1/user/contact"
    headers = {"token": str(localReadConfig.get_headers("token"))}
    res = requests.post(url=url, headers=headers, params=dict(zip(excle_titlelist, excle_datalist)))
    # res.json()返回python对象(一般返回体会被转化成字典)
    result = str(res.json().get("code"))
    return result


class TestContacts(unittest.TestCase):
    # 取出excle测试数据做参数化

    @parameterized.parameterized.expand(get_param("getContacts"))
    def test_get_contacts(self, *excle_data):
        '''地址搜索'''
        res = get_contacts(excle_data)
        self.assertEqual(res, excle_data[-1])

    @parameterized.parameterized.expand(get_param("addContacts"))
    @unittest.skip("")
    def test_add_contacts(self, *excle_data):
        res = add_contacts(excle_data)
        self.assertEqual(res, excle_data[-1])


if __name__ == '__main__':
    unittest.main(verbosity=1)

