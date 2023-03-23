import pytest
import allure
from common.read_config import ReadConfig
from common.request_builder import get_all_case_datas
from common.request_tool import CommonHttp
from common.request_builder import run_case_data
localReadConfig = ReadConfig()
CommonHttp = CommonHttp()


class Testtransports():
    @allure.title("{case_data[用例id]}")
    @pytest.mark.parametrize('case_data', get_all_case_datas("transports"))
    def test_transports(self, case_data):
        run_case_data(case_data)
