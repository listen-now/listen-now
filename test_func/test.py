#!/usr/bin/env python3
# @File:sjakhdh.py
# @Date:FileDate
# Author:Cat.1

# nohup sslocal -c /etc/shadowsocks.json /dev/null 2>&1 &

import qrcode

qr = qrcode.QRCode(version = None, error_correction = qrcode.constants.ERROR_CORRECT_L, box_size = 40, border=1);
qr.add_data("http://www.itdks.com/eventlist/detail/2269")
qr.make(fit = True) 
img = qr.make_image()
img.save("share.png")


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
