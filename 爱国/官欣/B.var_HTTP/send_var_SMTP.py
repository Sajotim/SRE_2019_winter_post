"""
from http://www.runoob.com/python/python-email.html
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

my_sender = '122688xxxx@qq.com'  # 发件人
my_pass = 'xxxxxxxxxxxxx'  # 发件人邮箱密码/授权码
my_user = '122688xxxx@qq.com'  # 收件人

def mail(fname):
    ret = True
    try:
        msg=MIMEMultipart()
        msg['From'] = formataddr(["FromPython", my_sender])
        msg['To'] = formataddr(["Miseria", my_user])  # 收件人
        msg['Subject'] = "PY发送邮件测试"
        msg.attach(MIMEText('最近一个月将过期的域名列表（见附件）', 'plain', 'utf-8'))

        att1=MIMEText(open(fname,'rb').read(),'base64','utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        att1["Content-Disposition"] = 'attachment; filename="domain.txt"'
        msg.attach(att1)

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()

    except Exception:
        ret = False
    return ret

def mail_text(fname):
    ret = True
    try:
        msg = MIMEText(open(fname,'rb').read(),'plain','utf-8')
        msg['From'] = formataddr(["FromPython", my_sender])
        msg['To'] = formataddr(["Miseria", my_user])
        msg['Subject'] = "PY发送邮件测试"

        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user, ], msg.as_string())
        server.quit()
    except Exception:
        ret = False
    return ret