import unittest
import parameterized
from common.read_config import ReadConfig
from common.request_builder import post_sheetname
from common.log_trace import case_log
localReadConfig = ReadConfig()


class TestgetTemps(unittest.TestCase):
    @parameterized.parameterized.expand(post_sheetname("getTemps"))
    def test_getTemps(self, *datalist):
        case_log(datalist)
