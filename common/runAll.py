import pytest
from pathlib import Path
from common import email_tool
from common.read_config import ReadConfig
from common.log_trace import mylog
from common.request_tool import CommonHttp
from common.case_builder import case_builder


# pro_dir = os.path.split(os.path.realpath(__file__))[0]   略复杂,弃用
# 当前文件路径的"爷爷"(上上级目录myTest)
pro_dir = Path(__file__).parents[1]
# caselist.txt 用于筛选运行的测试脚本 加#表示不用运行
casetxt_path = Path.joinpath(pro_dir, 'testcase/caselist.txt')
# testcase目录 用于存放测试脚本相关的文件
casefile_path = Path.joinpath(pro_dir, 'testcase')
# report目录 用于存放测试报告和日志文件
report_path = Path.joinpath(pro_dir, 'report')
localReadConfig = ReadConfig()
CommonHttp = CommonHttp()


class RunAllTests:
    def run(self):
        # 自动生成测试用例
        case_builder()
        # 先初始化ini文件中的token
        # CommonHttp.set_token()
        try:
            mylog().info("********TEST START********")
            pytest.main(['-vs', '../testcase'])
        except Exception as ex:
            mylog().error(str(ex))
        finally:
            mylog().info("********TEST END********")
        # 判断邮件发送开关
            on_off = localReadConfig.get_email("on_off")
            if on_off == "on":
                try:
                    email_tool.common_email()
                except Exception as ex:
                    mylog().error(str(ex))
                finally:
                    mylog().info("测试报告邮件已发送")

            elif on_off == 'off':
                mylog().info("邮件开关为off,不发送测试报告邮件")
            else:
                mylog().info("请检查邮件开关配置")


if __name__ == "__main__":
    RunAllTests().run()
