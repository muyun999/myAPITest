from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
from pathlib import Path
from common import read_config
from datetime import datetime
from common.log_trace import mylog
import re


pro_dir = Path(__file__).parents[1]
# 只要当天的测试报告
report_date = datetime.now().strftime('%Y%m%d')
# 测试报告路径
report_path = Path.joinpath(pro_dir, "report/testreport_" + report_date + ".html")


def common_email():
    rc = read_config.ReadConfig()
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
    report_result = email_text()
    text = f"{report_result}\n测试报告请见附件"
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    if report_path:
        send_file = MIMEApplication(open(report_path, 'rb').read())
        send_file.add_header('Content-Disposition', 'attachment', filename="测试报告.html")
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


def email_text():
    # 用于邮件正文显示测试概要结果
    # 兼容中文测试报告和英文报告
    textre = re.compile(r"attribute'><strong>(测试结果|Status) : </strong>(.+%)")
    with open(report_path, "rt", encoding="utf-8") as f:
        report_text = textre.findall(f.read())
    # return 测试结果: 共3，通过2，错误1，通过率 = 66.67 %
    return ":".join(report_text[0])


if __name__ == "__main__":
    # a = common_email()
    print(email_text())
