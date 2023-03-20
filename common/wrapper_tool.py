from functools import wraps
from common.log_trace import mylog
import traceback
from common.case_builder import post_sheetname


# 装饰器:用例执行日志跟踪+参数化测试(有些问题,不能一个用例多个结果 需要重写)
def log_execute_case(sheetname):
    def wrapper(func):
        # 被修饰的函数(wrapped) 的一些属性值赋值给 修饰器函数(wrapper)
        @wraps(func)
        def inner(*args, **kwargs):
            mylog().info(f"开始执行{func.__name__}模块")
            parame_list = post_sheetname(sheetname)
            for parame in parame_list:
                mylog().info(f"开始执行{func.__name__}中{parame[0]}的用例")
                mylog().info(f"参数为:{parame[1:]}")
                try:
                    func(self='', datalist=parame, **kwargs)
                except Exception as ex:
                    mylog().info(f"执行{func.__name__}中{parame[0]}的用例出错啦")
                    # print(ex)
                    traceback.print_exc()
                else:
                    mylog().info(f"结束执行{func.__name__}中{parame[0]}的用例")
                    mylog().info(f"结束执行{func.__name__}模块")
        return inner
    return wrapper



