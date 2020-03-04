import requests
from common.excle_tool import *
from common.read_config import ReadConfig
from common.request_tool import CommonHttp
from common.log_trace import mylog

localReadConfig = ReadConfig()
CommonHttp = CommonHttp()


def post_sheetname(sheetname):
    # 组装excle中每行数据进行请求
    # 参数化数据  实际运行结果与预期结果比较

    # 所有名称列表
    excle_all_titlelist = get_title(sheetname)

    # 所有数据列表
    excle_all_datas = get_param(sheetname)

    # 所有实际结果和预期结果的列表
    datas_list = []

    for excle_one_data in excle_all_datas:
        all_params = dict(zip(excle_all_titlelist, excle_one_data))
        # 判断body中有token参数的情况,有的话就更新token
        if "token" in all_params:
            all_params["token"] = str(localReadConfig.get_headers("token"))
        all_request_params = get_request_dict(all_params, ["是否跳过(Y/N)", "请求类型", "接口名称", "期望code", "期望errmsg", "期望data包含的数据"])
        headers = {"token": str(localReadConfig.get_headers("token"))}
        # excle_all_titlelist = get_title(sheetname)
        url_name = all_params.get("接口名称")
        if not url_name:
            mylog().info(f"{sheetname}中缺少接口名称")
            continue
        else:
            url = CommonHttp.set_url(url_name)
        request_method = all_params.get("请求类型")
        if not request_method:
            mylog().info(f"{sheetname}中缺少请求方法")
            # 如果发生错误就传个错误信息,这样可以统计到测试报告中
            datas_list.append(f"(错误用例){sheetname}中缺少请求方法")
            continue
        else:
            if request_method == "get":
                res = requests.get(url=url, headers=headers, params=all_request_params)
            elif request_method == "post":
                res = requests.post(url=url,  headers=headers, data=all_request_params)
            elif request_method == "put":
                res = requests.put(url=url,  headers=headers, data=all_request_params)
            elif request_method == "delete":
                res = requests.delete(url=url,  headers=headers, data=all_request_params)
            else:
                mylog().info(f"未知的请求方法:{request_method}")
                # 如果发生错误就传个错误信息,这样可以统计到测试报告中
                datas_list.append(f"(错误用例)未知的请求方法:{request_method}")
                continue
        casename = all_params.get("用例名称")
        mylog().info(f"用例名称:{casename},请求url为:{url},请求方法为:{request_method},请求参数为:{all_request_params}")
        mylog().info(f"接口返回值{res.json()}")
        # unicode转中文
        result = res.text.encode('utf-8').decode("unicode_escape")
        result_code = str(res.json().get("code"))
        result_errmsg = str(res.json().get("errmsg"))
        # 实际结果的列表
        result_list = [result_code, result_errmsg, result]
        # 实际结果和预期结果的列表
        data_list = [excle_one_data[0]] + excle_one_data[-3:] + result_list
        datas_list.append(data_list)
    return datas_list


def get_request_dict(mydict, delkeyslist):
    # dict.copy()一级目录是深拷贝 二级目录是浅拷贝
    newdict = mydict.copy()
    for i in delkeyslist:
        del newdict[i]
    return newdict


if __name__ == '__main__':
    # unittest.main(verbosity=2)
   print(post_sheetname("getFormals"))
