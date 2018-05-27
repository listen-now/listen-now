# POP3/SMTP服务 jekqrszpatkjbecb

from email.mime.text import MIMEText
import smtplib


msg_from = "1069954477@qq.com"
passwd = "jekqrszpatkjbecb"
# 输入收件人地址:
msg_to = "zhuyuefeng0@gmail.com"
# 输入SMTP服务器地址:
smtp_server = "smtp.qq.com"

subject = "测试专用" 
content = "厉害了我的哥"
msg = MIMEText(content)
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to

server = smtplib.SMTP_SSL("smtp.qq.com", 465)
print(server.set_debuglevel(1))
server.login(msg_from, passwd)
server.sendmail(msg_from, msg_to, msg.as_string())
server.quit()



