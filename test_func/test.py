#!/usr/bin/env python3
# @File:sjakhdh.py
# @Date:FileDate
# Author:Cat.1
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


pop3_server = "pop.gmail.com"
server = poplib.POP3_SSL(pop3_server)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))
email       = "zhuyuefeng0@gmail.com"
password = "eibZLC123"
# 身份认证:
server.user(email)
server.pass_(password)

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                try:
                    content = content.decode(charset)
                except LookupError:
                    print("邮件内容含有非UTF-8信息，无法解析。")
                else:
                    print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
                print('%sAttachment: %s' % ('  ' * indent, content_type))


# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
index = len(mails)
resp, lines, octets = server.retr(index)
msg_content = b'\r\n'.join(lines).decode('utf-8')
# 稍后解析出邮件:

msg = Parser().parsestr(msg_content)
print_info(msg)

# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
server.quit()

















# import qrcode

# qr = qrcode.QRCode(version = None, error_correction = qrcode.constants.ERROR_CORRECT_L, box_size = 40, border=1);
# qr.add_data("http://www.itdks.com/eventlist/detail/2269")
# qr.make(fit = True) 
# img = qr.make_image()
# img.save("share.png")


# import requests
# import threading
# from time import ctime,sleep



# def loop(name):
#     global i, a
#     global lock
#     while i<10:
#         print(name)
#         a = 3
#         i+=1

# i=0
# threads = []
# t1 = threading.Thread(target=loop,args=("t1",))
# threads.append(t1)
# t2 = threading.Thread(target=loop,args=("t2",))
# threads.append(t2)


# for t in threads:
#     t.start()
# t.join
# print(a)
