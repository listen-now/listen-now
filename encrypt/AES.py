#!usr/bin/env python3
# @File:AES.py
# @Date:2018/5/8
# Author:Cat.1

import os
import base64
import json
import binascii
from Crypto.Cipher import AES
import urllib.parse


enc_sec_key = '2d48fd9fb8e58bc9c1f14a7bda1b8e49a3520a67a2300a1f73766caee29\
f2411c5350bceb15ed196ca963d6a6d0b61f3734f0a0f4a172ad853f16dd06018bc5ca8fb64\
0eaa8decd1cd41f66e166cea7a3023bd63960e656ec97751cfc7ce08d943928e9db9b35400f\
f3d138bda1ab511a06fbee75585191cabe0e6e63f7350d6'

nonce       = b'0CoJUm6Qyw8W8jud'
sec_key     = b'a8LWv2uAtXjzSfkQ'

"""
接收网易API返回的json内容, 
进行AES加密后构造新的json_data返回,
用于请求播放地址.
"""
def encrypted_request(text):
    # sec_key           = create_secret_key(16)
    enc_text            = aes_encrypt(aes_encrypt(text, nonce), sec_key)
    url_encode_enc_text = urllib.parse.quote(enc_text)
    # 对生成的enc_text进行urlencode编码
    data = 'params=' + url_encode_enc_text + '&' + 'encSecKey=' + enc_sec_key
    # 构造str(requests.post方法不需要loads封装json文件, 直接返回即可)
    return data


def aes_encrypt(text, sec_key):
    pad = 16 - len(text) % 16
    text = text + chr(pad) * pad
    # 标准补码设置()
    encryptor   = AES.new(sec_key, AES.MODE_CBC, b'0102030405060708')
    # 设置加密模式, 加密key内容, iv量
    cipher_text = encryptor.encrypt(text.encode(encoding = 'UTF-8'))
    # 传入的参数使用bytes格式, 进行加密
    cipher_text = base64.b64encode(cipher_text).decode('utf-8')
    # 传出的结果使用base64编码
    return cipher_text



if __name__ == '__main__':
    
    print(encrypted_request("{\"ids\":\"[484730184]\",\"br\":128000,\"csrf_token\":\"\"}"))


