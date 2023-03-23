from common.log_trace import mylog


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
            mylog().error(f">>>>>>用例id:{datadict['用例id']}_{datadict['用例说明']}断言失败")
            # 因为做了异常处理,需要重新抛出异常,否则失败的用例会被当作成功
            raise AssertionError()
        else:
            mylog().info(f">>>>>>用例id:{datadict['用例id']}断言成功")
        finally:
            mylog().info(f">>>>>>结束执行用例id:{datadict['用例id']}")
    return wrapper



