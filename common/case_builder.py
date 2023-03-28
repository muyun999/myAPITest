from common.excel_tool import get_tables
from pathlib import Path
import os

# pro_dir = os.path.split(os.path.realpath(__file__))[0]   略复杂,弃用
# 当前文件路径的"爷爷"(上上级目录myTest)
pro_dir = Path(__file__).parents[1]
case_path = Path.joinpath(pro_dir, 'testcase')
demofile_path = Path.joinpath(pro_dir, 'common/test_Demo.py')
case_list = [i for i in os.listdir(case_path) if i.startswith("test")]


def case_builder():
    # 根据已有的test_Demo.py的内容,自动根据excel的表名生成测试用例脚本
    for table_name in get_tables():
        newfile = "test_"+table_name+".py"
        if newfile in case_list:
            continue
        else:
            os.chdir(case_path)
            with open(demofile_path, "r", encoding="utf-8") as f1, open(newfile, "w+", encoding="utf-8") as f2:
                for line in f1.readlines():
                    line = line.replace("Demo", table_name)
                    f2.write(line)


if __name__ == '__main__':
    case_builder()
