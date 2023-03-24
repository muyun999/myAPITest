import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from common.log_trace import *



def send_email():
    # 判断邮件发送开关
    on_off = rc.get_email("on_off")
    if on_off == "on":
        try:
            email_content()
        except Exception as ex:
            mylog().error(str(ex))
        finally:
            mylog().info("测试报告邮件已发送")

    elif on_off == 'off':
        mylog().info("邮件开关为off,不发送测试报告邮件")
    else:
        mylog().info("请检查邮件开关配置")


def email_content():
    smtpserver = rc.get_email("smtpserver")
    login_name = rc.get_email("login_name")
    login_password = rc.get_email("login_password")
    sender = rc.get_email("sender")
    receiver = rc.get_email("receiver")
    subject = rc.get_email("subject")

    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    # 构造文本
    text = "".join(log_analyse())+"\n运行日志请见附件"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    if logfile_path:
        send_file = MIMEApplication(open(logfile_path, 'rb').read())
        send_file.add_header('Content-Disposition', 'attachment', filename="接口自动化运行日志.log")
        msg.attach(send_file)
        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver)
        smtp.login(login_name, login_password)
        # 收件人多个时需要用列表
        smtp.sendmail(sender, receiver.split(";"), msg.as_string())
        smtp.quit()
    else:
        mylog().info("当天测试报告未生成")


if __name__ == "__main__":
    print(email_content())
