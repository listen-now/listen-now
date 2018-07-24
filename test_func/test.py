#!/usr/bin/env python3
# @File:sjakhdh.py
# @Date:FileDate
# Author:Cat.1

# nohup sslocal -c /etc/shadowsocks.json /dev/null 2>&1 &

# import qrcode

# qr = qrcode.QRCode(version = None, error_correction = qrcode.constants.ERROR_CORRECT_L, box_size = 40, border=1);
# qr.add_data("http://www.itdks.com/eventlist/detail/2269")
# qr.make(fit = True) 
# img = qr.make_image()
# img.save("share.png")

# from cryptography.fernet import Fernet, MultiFernet
# key1  = Fernet(Fernet.generate_key())
# key2  = Fernet(Fernet.generate_key())
# f     = MultiFernet([key1, key2])
# token = f.encrypt(b"Secret message!")
# print(token)
# print(f.decrypt(token))

# key3    = Fernet(Fernet.generate_key())
# f2      = MultiFernet([key3, key2, key1])
# rotated = f2.rotate(token)
# print(rotated)
# print(f2.decrypt(rotated))



#! /usr/bin/python3
from Crypto.Cipher import AES
from binascii import b2a_base64, a2b_base64
from cryptography.fernet import Fernet
# import os
 
# class AES_Crypt_Cookies(object):
#     def __init__(self,key):
#         self.mode = AES.MODE_CBC
#         self.key  = self.Pad_Key(key)

#     def Creat_text(self):
#     # 用js生成cookies信息

#         compile_js = execjs.compile("""function createGuid() {
#                                     return (((1 + Math.random()) * 0x10000) | 0).\
#                                     toString(16).substring(1);
#                                     }""")
#         guid = compile_js.call("createGuid") 

#         return guid

#     def Pad_Text(self,text):
#         text = bytes(text,encoding="utf8")
#         while len(text) % 16 != 0:
#             text += b'\0'
#         return text
#     def Pad_Key(self,key):
#         key = bytes(key, encoding="utf8")
#         while len(key) % 16 != 0:
#             key += b'\0'
#         return key
 
#     def encrypt(self,text):
#         texts = self.pad(text)
#         aes = AES.new(self.key, self.mode,self.key)
#         res = aes.encrypt(texts)
#         return str(b2a_base64(res),encoding= "utf-8")
 
#     def decrypt(self,text):
#         texts = a2b_base64(self.pad(text))
#         aes = AES.new(self.key, self.mode,self.key)
#         res = str(aes.decrypt(texts),encoding="utf8")
#         return res
 
# import rsa
 
# (pubkey, privkey) = rsa.newkeys(512)
# with open('../project/Helper/pub_valid.pem','w+') as f:
#     f.write(pubkey.save_pkcs1().decode())

# with open('pri_vaild.pem','w+') as f:
#     f.write(privkey.save_pkcs1().decode())


# if __name__ == "__main__":
#     # key = "fdsifekksonbn"

#     text = "Python123"
#     a = AES_Crypt_Cookies(key).encrypt(text)
#     b = AES_Crypt_Cookies(key).decrypt(a)
#     print(a)
#     print(b)
import datetime
outdate=datetime.datetime.today() + datetime.timedelta(days=2)


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
