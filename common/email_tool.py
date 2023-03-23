import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from common import read_config
from datetime import datetime
from common.log_trace import mylog

# 测试报告日志路径
pro_dir = Path(__file__).parents[1]
log_dir = Path.joinpath(pro_dir, "report")
log_name = "test_case_run_" + str(datetime.now().strftime("%Y%m%d")) + ".log"
logfile_path = Path.joinpath(log_dir, log_name)


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
    text = f"{report_result}\n运行日志请见附件"
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


def email_text():
    # 用于邮件正文显示测试概要结果
    if Path(logfile_path).exists():
        with open(logfile_path, "rt", encoding="utf-8") as f:
            log_text = str(f.readlines())
            fail_case = re.findall("ERROR : >>>>>>用例id:(.*?)断言失败", log_text)
            fail_case = "\n".join(fail_case)
            success_num = log_text.count("断言成功")
            fail_num = log_text.count("断言失败")
            total_num = success_num+fail_num
            pass_rate = format(success_num / total_num, '.2%')
            return f"测试结果: 共{total_num}，通过:{success_num}，失败:{fail_num}，通过率:{pass_rate}\n" \
                f'其中失败用例为:\n{fail_case}'


if __name__ == "__main__":
    print(email_text())
