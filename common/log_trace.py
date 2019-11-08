import logging
from datetime import datetime
from pathlib import Path
import unittest
import inspect
import os
pro_dir = Path(__file__).parents[1]
log_dir = Path.joinpath(pro_dir, "report")
log_name = "test_case_run_" + str(datetime.now().strftime("%Y%m%d")) + ".log"
logfile_path = Path.joinpath(log_dir, log_name)
# 判断是否已经存在当天的日志,有就重新开始记录
if Path(logfile_path).exists():
    os.remove(logfile_path)


def mylog():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # 用前判断  不然会造成日志重复打印的问题
    if not logger.handlers:
        # 创建一个handler用于写入日志文件  指定encoding是为了防止打开日志文件时内容乱码
        file_handler = logging.FileHandler(logfile_path, encoding="utf-8")
        # 创建一个handler用于输出到控制台
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger


def case_log(datalist):
    """用来记录用例执行情况
        datalist  列表   excle中每行元素"""
    # inspect.stack()用来获取调用栈
    mylog().info(f"开始执行{inspect.stack()[1][3]}中 [{datalist[0]}] 的用例")
    expect = datalist[1:3]
    real = datalist[-2:]
    mylog().info(f"预期结果{expect},实际结果{real}")
    unittest.TestCase().assertTupleEqual(expect, real)
    mylog().info(f"完成执行{inspect.stack()[1][3]}中 [{datalist[0]}] 的用例")
    mylog().info("=================================")


if __name__ == "__main__":
    pass
