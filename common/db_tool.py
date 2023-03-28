import os
import pymysql
from common.log_trace import mylog
from datetime import datetime
from pathlib import Path
from common.read_config import ReadConfig
from sshtunnel import SSHTunnelForwarder
localReadConfig = ReadConfig()
pro_dir = Path(__file__).parents[1]
# 数据库备份路径
backup_path = Path.joinpath(pro_dir, 'backup')


class DatabaseBR:
    """数据库备份、恢复"""
    sql_text = "show databases;"
    host = ReadConfig().get_db('mysql_host')
    port = ReadConfig().get_db('mysql_port')
    user = ReadConfig().get_db('mysql_user')
    passwd = ReadConfig().get_db('mysql_passwd')
    ssh_host = ReadConfig().get_db('ssh_host')
    ssh_port = ReadConfig().get_db('ssh_port')
    ssh_user = ReadConfig().get_db('ssh_user')
    ssh_passwd = ReadConfig().get_db('ssh_passwd')

    # 使用密钥文件登录服务器连接方式操作数据库
    # 数据库放在了服务器A上，只允许服务器B来访问，而我在机器C上，可以通过ssh连接服务器B
    def execsql(self):
        server = SSHTunnelForwarder(
            # 运萌测试库
            ssh_address_or_host=(self.ssh_host, self.ssh_port),  # B机器(跳板机)ssh主机名或IP地址
            ssh_username=self.ssh_user,  # B机器(跳板机)ssh用户名
            ssh_password=self.ssh_passwd,  # B机器(跳板机)ssh密码
            remote_bind_address=(self.host, self.port))  # A机器的数据库主机名或IP地址-MySQL服务器

        server.start()
        myconn = pymysql.connect(
            user=self.user,  # A机器的数据库用户名-MySQL服务器账户
            passwd=self.passwd,  # A机器的数据库密码-MySQL服务器密码
            host="127.0.0.1",  # 此处必须是127.0.0.1，代表C机器
            port=server.local_bind_port
            # ,db='mydb' # 可以限定，只访问特定的数据库,否则需要在mysql的查询或者操作语句中，指定好库名
        )
        cursor = myconn.cursor()
        # 后续数据库操作...
        cursor.close()
        myconn.commit()
        myconn.close()
        server.stop()

    def backing(self):
        """数据库备份"""
        mylog().info(">>>>>>>进入执行备份数据库的方法")
        mylog().info(">>>>>>>正在连接数据库……")
        try:
            con = pymysql.connect(user=self.user,
                                  password=self.passwd,
                                  host=self.host,
                                  port=self.port)
            cur = con.cursor()
            cur.execute(self.sql_text)
            mylog().info(">>>>>>>正在执行sql……")
            dbs = cur.fetchall()
            for db in dbs:
                db = list(db)[0]
                if db not in ['information_schema', 'mysql', 'performance_schema', 'sys']:
                    backup_name = db+str(datetime.now().strftime("%Y%m%d"))+".sql"
                    backup_sql_path = Path.joinpath(backup_path, backup_name)
                # 判断是否已经存在当天的备份数据,没有才备份
                    if Path(backup_sql_path).exists():
                        mylog().info(f">>>>>>>{backup_sql_path}已存在,无需备份")
                        continue
                    else:
                        mylog().info(f">>>>>>>{backup_sql_path}不存在，开始备份……")
                        dumps = f"mysqldump -u {self.user} -p {self.passwd} -h {self.host} -P{self.port} -E -R {db} > {backup_name}"
                        os.system(dumps)
            cur.close()
            mylog().info(">>>>>>>提交事务")
            con.commit()
        except Exception as ex:
            mylog().error(">>>>>>>操作数据库备份时发生未知错误!")
            mylog().error(str(ex))
        finally:
            con.close()
            mylog().info(">>>>>>>关闭数据库连接")

    def recovering(self):
        """数据库恢复"""
        sql_files = os.listdir(backup_path)
        mylog().info(f">>>>>>>当前备份的sql文件有：{sql_files}")
        for sql_file in sql_files:
            dbname = sql_file.split('.')[0]
            try:
                mylog().info(">>>>>>>开始恢复……")
                recover = f"mysql -u {self.user} -p {self.passwd} -h {self.host} -P{self.port} {dbname} < {sql_file}"
                os.system(recover)
                mylog().info(f">>>>>>>{dbname}数据已恢复！")
            except Exception as ex:
                mylog().error(f">>>>>>>{dbname}恢复失败")
                mylog().error(str(ex))


if __name__ == '__main__':
    pass
