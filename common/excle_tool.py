import xlrd
from pathlib import Path


pro_dir = Path(__file__).parents[1]
excle_path = Path.joinpath(pro_dir, "excle_data/lineCase_old.xlsx")


def get_tables():
    data = xlrd.open_workbook(excle_path)
    return data.sheet_names()


def get_title(sheetname, *delcols):
    """
    从excle中获取指定工作表的表头
    :param sheetname: sheet工作表名称
    :param delcol: 不需要的参数列
    :return: 返回参数名列表
    """
    data = xlrd.open_workbook(excle_path)
    table = data.sheet_by_name(sheetname)
    title = table.row_values(0)
    if delcols:
        for delcol in delcols:
            title.remove(delcol)
    return title


# 取工作表中的请求类型
def get_method(sheetname):
    data = xlrd.open_workbook(excle_path)
    table = data.sheet_by_name(sheetname)
    methodnames = table.col_values(2, 1)
    return methodnames


# 取工作表中的接口名称
def get_interface(sheetname):
    data = xlrd.open_workbook(excle_path)
    table = data.sheet_by_name(sheetname)
    interfacenames = table.col_values(3, 1)
    return interfacenames


# 取工作表中的是否Cookie(默认Y)
def get_iscookie(sheetname):
    data = xlrd.open_workbook(excle_path)
    table = data.sheet_by_name(sheetname)
    return table.cell_value(1, 4)


# 取工作表中的是否跳过列(默认N)
def get_isskip(sheetname):
    data = xlrd.open_workbook(excle_path)
    table = data.sheet_by_name(sheetname)
    # 标题去掉,只取值(返回列表)
    return table.col_values(1, 1)


def get_param(sheetname, *delcol):
    """
    :param sheetname: sheet工作表名称
    :param delcol: 需要删除的表格列名
    :return: 返回表格每行数据组成的列表(不含需要跳过标志的数据)
    """
    # 所有行的数据列表
    paramlist = []
    del_index_list = []
    data = xlrd.open_workbook(excle_path)
    table = data.sheet_by_name(sheetname)
    # 获取该sheet中的有效行数
    rownum = table.nrows
    # 跳过标题行,从1开始取
    for i in range(1, rownum):
        # 得到每行数据组成的元素
        paramlist.append(table.row_values(i))
    if delcol:
        for i in range(len(delcol)):
            # 得到需要删除的元素索引
            del_index_list.append(table.row_values(0).index(delcol[i]))
        # 把索引从大到小排序,防止下面进行操作的时候发生越界错误
        del_index_list.sort(reverse=True)
        for del_index in del_index_list:
            for j in range(0, rownum-1):
                # 删除列名所在的列元素
                del paramlist[j][del_index]
    # 去掉含跳过标志的数据
    skiplist = get_isskip(sheetname)
    # 倒排是为了防止del的时候越界
    for i in range(len(skiplist)-1, -1, -1):
        if skiplist[i] == "Y":
            del paramlist[i]
    return paramlist


if __name__ == "__main__":
    # get_title("login")
    # get_param("getRecode", "用例名称", "是否跳过(Y/N)", "请求类型", "接口名称", "Cookie(Y/N)")
    pass

