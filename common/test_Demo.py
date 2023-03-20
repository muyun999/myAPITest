import pytest
from common.read_config import ReadConfig
from common.request_builder import get_all_case_datas
from common.request_tool import CommonHttp
from common.request_builder import run_case_data
localReadConfig = ReadConfig()
CommonHttp = CommonHttp()


class TestDemo():
    @pytest.mark.parametrize('case_data', get_all_case_datas("Demo"))
    def test_line(self, case_data):
        run_case_data(case_data)
