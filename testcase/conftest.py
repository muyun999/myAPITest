import pytest
from common.log_trace import mylog
from common.request_tool import CommonHttp
from common.db_tool import DatabaseBR


@pytest.fixture(autouse=True, scope='session')
def test_before():
    mylog().info("************开始数据库备份执行******************")
    # DatabaseBR().backing()
    # CommonHttp().set_token()
    yield
    mylog().info("********************开始数据库恢复执行**************")
    # DatabaseBR().recovering()

