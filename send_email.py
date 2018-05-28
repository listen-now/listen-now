#!usr/bin/env python3
# @File:send_email.py
# @Date:2018/05/27
# Author:Cat.1

from email.mime.text import MIMEText
import smtplib
import config

msg_from       = config.getConfig("send_email", "msg_from")
passwd         = config.getConfig("send_email", "passwd")
msg_to         = config.getConfig("send_email", "msg_to")
smtp_server    = config.getConfig("send_email", "smtp_server")
subject        = "测试专用" 
content        = "厉害了我的哥"
msg            = MIMEText(content)
msg['Subject'] = subject
msg['From']    = msg_from
msg['To']      = msg_to
server         = smtplib.SMTP_SSL(smtp_server, 465)
server.login(msg_from, passwd)
server.sendmail(msg_from, msg_to, msg.as_string())
server.quit()
# print(server.set_debuglevel(1))



