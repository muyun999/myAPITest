import requests
from common import global_data as gbl
from common.excel_tool import *
from common.request_tool import CommonHttp
from common.log_trace import *

CommonHttp = CommonHttp()


# excel中所有的数据组成的字典列表
def get_all_case_datas(sheetname):
    excel_titlelist = get_title(sheetname)
    # 所有数据列表
    excel_all_datas = get_param(sheetname)
    # 所有case组成的列表
    all_case_datas = []
    for excel_one_data in excel_all_datas:
        data_dict = dict(zip(excel_titlelist, excel_one_data))
        # 去掉跳过标记为Y的数据
        if data_dict.get("是否跳过(Y/N)").strip().upper() == 'Y':
            continue
        for title_name in ("接口名称", "url端口号", "请求类型"):
            if not data_dict.get(title_name):
                mylog().error(data_dict.get("用例id")+f"中缺少{title_name}参数")
                continue
        data_port = data_dict.get("url端口号")
        api_name = data_dict.get("接口名称")
        url_port = ":" + data_port if data_port else ""
        url = CommonHttp.set_url(url_port + api_name)
        data_dict["url"] = url
        if data_dict.get("headers"):
            data_dict["headers"] = transform_request_data(data_dict.get("headers"))
        if data_dict.get("request_data"):
            data_dict["request_data"] = transform_request_data(data_dict.get("request_data"))
        all_case_datas.append(data_dict)
    return all_case_datas


# 跑单条数据
@log_execute_case
def run_case_data(case_data):
    # 替换掉接口请求和预期值关联中的参数)
    if gbl.globals_vars:
        for _key, _value in gbl.globals_vars.items():
            if case_data.get("request_data") and str(case_data.get("request_data")).find(_key) != -1:
                case_data["request_data"] = eval(str(case_data["request_data"]).replace(_key, _value))
            if str(case_data.get("expect_data")).find(_key) != -1:
                case_data["expect_data"] = str(case_data["expect_data"]).replace(_key, _value)
    request_method = case_data.get("请求类型")
    if request_method.lower() not in ("get", "post", "put", "delete"):
        mylog().error(f">>>>>>>未知的请求方法:{request_method},目前仅支持get/post/put/delete")
    if request_method.lower() == "get":
        res = requests.get(url=case_data["url"], headers=case_data["headers"], params=case_data["request_data"]).text
    else:
        res = requests.request(request_method.lower(), url=case_data["url"], headers=case_data["headers"],
                               data=case_data["request_data"]).text
    case_data['response'] = res
    res_expressions = case_data.get("提取表达式")
    if res_expressions:
        res_expressions_list = res_expressions.split("\n")
        for res_expression in res_expressions_list:
            expression_str = res_expression.split("=")
            expression_key = expression_str[0]
            expression_value = expression_str[1]
            if re.findall(expression_value, str(res)):
                gbl.globals_vars[expression_key] = re.findall(expression_value, str(res))[0]
            else:
                mylog().error("==============没有在返回值中找到提取值==============")
    assert re.search(case_data.get("expect_data"), res, flags=re.S) is not None


if __name__ == '__main__':
   print(get_all_case_datas("new_model"))
