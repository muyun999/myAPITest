import unittest
import parameterized
from common.read_config import ReadConfig
from common.case_builder import post_sheetname
from common.log_trace import case_log
localReadConfig = ReadConfig()


class TestTrucks(unittest.TestCase):
    @parameterized.parameterized.expand(post_sheetname("getTrucks"))
    def test_get_trucks(self, *datalist):
        case_log(datalist)


if __name__ == '__main__':
    # unittest.main(verbosity=2)
    print(post_sheetname("getTrucks")[0][1:3])

