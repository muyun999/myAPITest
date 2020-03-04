import unittest
from pathlib import Path
from common import HTMLTestRunner_old, HTMLTestRunnerCN, HTMLTestRunnerEN
from datetime import datetime
from common import email_tool
from common.read_config import ReadConfig
from common.log_trace import mylog
from common.request_tool import CommonHttp


# pro_dir = os.path.split(os.path.realpath(__file__))[0]  os的方法太麻烦 弃用
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
    # 获取caselist.txt中不带#的测试用例
    def set_case_list(self):
        caselist = []
        with open(casetxt_path, 'r') as f:
            # 类似['#user/testContacts.py\n', 'user/testTrucks.py\n']
            all_cases_list = f.readlines()
        for case in all_cases_list:
            if not case.startswith("#"):
                caselist.append(case.replace("\n", ""))
        # 没啥作用 就是为了展示好看点,做了换行操作
        casename = "\n".join(caselist)
        mylog().info(f"本次需要运行的脚本:\n{casename}")
        return caselist

    def set_case_suite(self):
        suitelist = []
        suite = unittest.TestSuite()
        # 取出不带"#"用来跑测试数据
        for case in self.set_case_list():
            all_case = unittest.defaultTestLoader.discover(casefile_path, pattern=case.split("/")[-1])
            suitelist.append(all_case)
        for case in suitelist:
            suite.addTests(case)
        # suite.addTests(suitelist)
        return suite

    def run(self):
        # 判断是否需要验证码 如果不需要验证码,就调登入接口获取并更新token
        if localReadConfig.get_login("need_Verification_Code") == "N":
            # 先初始化ini文件中的token
            CommonHttp.set_token()
        try:
            suite = self.set_case_suite()
            mylog().info("********TEST START********")
            reportname = f"testreport_{datetime.now().strftime('%Y%m%d')}.html"
            # 报告格式  支持老版本,优化后的中文版和英文版
            report_form = ReadConfig().get_reportform("testreport_form")
            with open(report_path/reportname, 'wb') as fp:
                if report_form == "CN" or not report_form:
                    runner = HTMLTestRunnerCN.HTMLTestReportCN(
                        stream=fp,
                        # description='所有测试情况',
                        # tester="muyun"   不写默认QA
                        title="自动化测试报告")
                elif report_form == "EN":
                    runner = HTMLTestRunnerEN.HTMLTestReportEN(stream=fp, title="自动化测试报告")
                else:
                    # 老版本
                    runner = HTMLTestRunner_old.HTMLTestReport(stream=fp, title="{Test Report}")
                runner.run(suite)
        except Exception as ex:
            mylog().error(str(ex))
        finally:
            mylog().info("********TEST END********")
        # 判断邮件发送开关
            on_off = localReadConfig.get_email("on_off")
            if on_off == "on":
                mylog().info("测试报告邮件已发送")
                email_tool.common_email()
            elif on_off == 'off':
                mylog().info("邮件开关为off,不发送测试报告邮件")
            else:
                mylog().info("请检查邮件开关配置")


if __name__ == "__main__":
    RunAllTests().run()
