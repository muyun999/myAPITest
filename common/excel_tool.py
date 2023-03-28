import xlrd
from pathlib import Path
from common.read_config import ReadConfig
localReadConfig = ReadConfig()

pro_dir = Path(__file__).parents[1]
excel_path = Path.joinpath(pro_dir, "excel_data/case_data.xls")


def get_tables():
    data = xlrd.open_workbook(excel_path)
    return data.sheet_names()


def get_title(sheetname):
    """
    从excel中获取指定工作表的表头
    :param sheetname: sheet工作表名称
    :return: 返回参数名列表
    """
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name(sheetname)
    title = table.row_values(0)
    return title


def get_param(sheetname):
    """
    :param sheetname: sheet工作表名称
    :return: 返回表格每行数据组成的列表
    """
    # 所有行的数据列表
    paramlist = []
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_name(sheetname)
    # 获取该sheet中的有效行数
    rownum = table.nrows
    # 跳过标题行,从1开始取
    for i in range(1, rownum):
        # 得到每行数据组成的元素
        paramlist.append(table.row_values(i))
    return paramlist


def transform_request_data(cell_data):
    '''
    对excel中的请求数据做处理,变成字典格式,例如请求数据格式为这样(取自请求参数):
    group_status: 1,2,3
    trans_number: 10011001
    cq_number:
    city: 杭州
    is_bind_driver: 1
    处理后变为:
    {'group_status': '1,2,3', 'trans_number': '10011001', 'cq_number': '', 'city': '杭州', 'is_bind_driver': '1'}
    '''
    # 如果数据本身是个字典格式的,转码下返回(看具体项目编码格式)
    # if cell_data.startswith("{") and cell_data.endswith("}"):
    if cell_data[0] in ('[', '{') and cell_data[-1] in (']', '}'):
        return cell_data.encode("utf-8").decode("latin1")
    else:
        datas = cell_data.split('\n')
        key_list, value_list = [], []
        for data in datas:
            # 分隔一次,防止值里带有":"
            _data_list = data.split(":", 1)
            key = _data_list[0].strip()
            value = _data_list[1].strip()
            key_list.append(key)
            value_list.append(value)
        data_dict = dict(zip(key_list, value_list))
        # 把配置文件中的token直接替换掉,防止这个token值过期
        if data_dict.get('token'):
            data_dict['token'] = str(localReadConfig.get_headers("token"))
        # 对请求头中的Authorization: Bearer ca6628b2964c4a6e92e860d40abc3a也直接替换掉
        if data_dict.get('Authorization'):
            data_dict['Authorization'] ="Bearer "+ str(localReadConfig.get_headers("token"))
        return data_dict


if __name__ == "__main__":
    print(transform_request_data('start_time : 2023-12-03 03:02:07'.split()))


