import logging
import re
from datetime import datetime
from pathlib import Path
from common import read_config

rc = read_config.ReadConfig()
pro_dir = Path(__file__).parents[1]
log_dir = Path.joinpath(pro_dir, "report")
log_name = "test_case_run_" + str(datetime.now().strftime("%Y%m%d")) + ".log"
logfile_path = Path.joinpath(log_dir, log_name)


def mylog():
    lever = rc.get_inidata('LOGGING', 'lever')
    logger = logging.getLogger()
    logger.setLevel(lever)
    # 用前判断  不然会造成日志重复打印的问题
    if not logger.handlers:
        # 创建一个handler用于写入日志文件 w+覆盖同名日志 指定encoding是为了防止打开日志文件时内容乱码
        file_handler = logging.FileHandler(logfile_path, mode='w+',encoding="utf-8")
        # 创建一个handler用于输出到控制台
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s : %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


# 统计日志结果
def log_analyse():
    # 用于邮件正文/钉钉上显示测试概要结果
    content = []
    if Path(logfile_path).exists():
        with open(logfile_path, "rt", encoding="utf-8") as f:
            log_text = str(f.readlines())
            fail_case = re.findall("ERROR : >>>>>>用例id:(.*?)断言失败", log_text)
            fail_case = "\n".join(fail_case)
            success_num = log_text.count("断言成功")
            fail_num = log_text.count("断言失败")
            total_num = success_num+fail_num
            pass_rate = format(success_num / total_num, '.2%')
            result = f"测试结果: 共{total_num}，通过:{success_num}，失败:{fail_num}，通过率:{pass_rate}\n"
            fail_case = f"其中失败用例为:\n{fail_case}"
            content.append(result)
            if fail_num != 0:
                content.append(fail_case)
            return content


# 装饰器:用例执行时的日志跟踪
def log_execute_case(func):
    def wrapper(*args, **kwargs):
        datadict = args[0]
        try:
            mylog().info(f">>>>>>>开始执行用例:{datadict['用例id']}_{datadict['用例说明']}")
            func(*args, **kwargs)
        except AssertionError:
            mylog().info(f">>>>>>>url为:{datadict['url']}")
            mylog().info(f">>>>>>>请求头参数为:{datadict.get('headers')}")
            mylog().info(f">>>>>>>请求参数为:{datadict['request_data']}")
            mylog().info(f">>>>>>>请求返回值为:{datadict['response']}")
            mylog().info(f">>>>>>>预期值为:{datadict['expect_data']}")
            mylog().info(f">>>>>>>返回值为:{datadict['response']}")
            mylog().error(f">>>>>>>用例id:{datadict['用例id']}_{datadict['用例说明']}断言失败")
            # 因为做了异常处理,需要重新抛出异常,否则失败的用例会被当作成功
            raise AssertionError()
        else:
            mylog().info(f">>>>>>>用例id:{datadict['用例id']}断言成功")
        finally:
            mylog().info(f">>>>>>>结束执行用例id:{datadict['用例id']}")
            mylog().info("************************************************")
    return wrapper


if __name__ == '__main__':
    a = "".join(log_analyse())
    print(a)


