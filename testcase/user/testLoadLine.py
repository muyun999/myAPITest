import unittest
import parameterized
import requests
from common.excle_tool import get_title, get_param
from common.read_config import ReadConfig

localReadConfig = ReadConfig()


# 货主工作台公路运单查询接口
def get_loadline(paramslist):
    excle_titlelist = get_title("loadline", "result")
    excle_datalist = list(paramslist)
    url = "http://workbench.optima-trans.net/v1/order/lands"
    headers = {"token": str(localReadConfig.get_headers("token"))}
    res = requests.get(url=url, headers=headers, params=dict(zip(excle_titlelist, excle_datalist)))
    result = str(res.json().get("data").get("total"))
    return result


class TestLine(unittest.TestCase):
    # 取出excle测试数据做参数化
    @parameterized.parameterized.expand(get_param("loadline", "result"))
    def test_get_loadline(self, *excle_data):
        res = get_loadline(excle_data)
        self.assertEqual(res, excle_data[-1])


if __name__ == '__main__':
    unittest.main(verbosity=2)

