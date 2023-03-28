import pytest
import os
from common import email_tool
from common import dingding_tool
from common.log_trace import *
from common.case_builder import case_builder


class RunAllTests:
    def run(self):
        try:
            # 自动生成测试用例
            case_builder()
            mylog().info("********TEST START********")
            # pytest.main(['-vs', r'C:\Users\JinXy\PycharmProjects\myAPITest\testcase'])
            # pytest.main(['-vs', '../testcase'])
            pytest.main(['-vs', '../testcase', '--alluredir', '../json_temp', '--clean-alluredir'])
            os.system('allure generate ../json_temp -o ../report --clean')
        except Exception as ex:
            mylog().error(str(ex))
        finally:
            mylog().info("********TEST END********")

        # 发送邮件
            email_tool.send_email()
        #  发送钉钉
            dingding_tool.send_dingding()


if __name__ == "__main__":
    RunAllTests().run()
