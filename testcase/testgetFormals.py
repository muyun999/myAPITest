import unittest
import parameterized
from common.read_config import ReadConfig
from common.request_builder import post_sheetname
from common.log_trace import case_log
localReadConfig = ReadConfig()


class TestgetFormals(unittest.TestCase):
    @parameterized.parameterized.expand(post_sheetname("getFormals"))
    def test_getFormals(self, *datalist):
        case_log(datalist)
