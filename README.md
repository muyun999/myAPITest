# myAPITest  
接口自动化项目  
功能:  
1,只需要按照已有的excel格式编写测试数据就可以自动的创建测试用例脚本  
2,自动生成测试报告并根据配置的收件人自动发送邮件(前提打开配置文件中的发送开关)  
3,支持各种形式的接口方式,请求直接复制页面数据即可
4,支持接口间的关联
5,支持预期值部分匹配返回值进行校验

文件说明:
1,使用python3.8编写,请使用3.8及以上版本,防止某些模块不能使用
2,主函数为runAll.py
3,脚本主入口为common的runAll.py文件
4,测试报告的生成的地址为report目录下,在这个目录下你也可以看到运行的日志信息
5,case_builder可以根据demo自行把excle中所有表的数据生成对应的测试文件
6,可以对自动化的数据进行数据库备份和恢复


注意事项:
1,excle中的预期值顺序要和返回值保持一致,不需要验证的值使用.*代替,注意预期值键值对冒号右边的空格
2,请求值直接复制页面的请求就可以了,不需要加{}和""
3,提取表达式使用的是正则表达式,注意键值对冒号右边的空格
4,excle最好需要用xls格式,版本较高的xlrd库不支持xlsx格式

其他:
如果运行中有什么不懂的地方或者有更好的优化的地方,可以联系我:805034884@qq.com
