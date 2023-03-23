import logging
from datetime import datetime
from pathlib import Path
from common import read_config
import os
pro_dir = Path(__file__).parents[1]
log_dir = Path.joinpath(pro_dir, "report")
log_name = "test_case_run_" + str(datetime.now().strftime("%Y%m%d")) + ".log"
logfile_path = Path.joinpath(log_dir, log_name)
# 判断是否已经存在当天的日志,有就重新开始记录
# if Path(logfile_path).exists():
#     os.remove(logfile_path)

def mylog():
    rc = read_config.ReadConfig()
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


if __name__ == '__main__':
    pro_dir = Path(__file__).parents[1]
    log_dir = Path.joinpath(pro_dir, "report")
    log_name = "test_case_run_" + str(datetime.now().strftime("%Y%m%d")) + ".log"
    logfile_path = Path.joinpath(log_dir, log_name)


