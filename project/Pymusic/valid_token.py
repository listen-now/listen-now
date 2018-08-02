#__date__2018/7/27
#__file__valid_token
#__author__Msc
# coding=utf-8

import requests
import rsa
import base64
import json
def valid_token():
    r = requests.get("http://zlclclc.cn/get_token")
    s = eval(r.json()["signature"])
    signature = base64.decodestring(s)      
    crypto = r.json()["token_message"]
    message = crypto[2:-6]+'\n'     
    with open('pubkey.pem','r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())        
    
    v = rsa.verify(message.encode(), signature, pubkey)     
    
    try:
        rsa.verify(message.encode(), signature, pubkey)
        sign_valid = 1
    except:
        sign_valid = 0      
    token_message = crypto[2:110]+'\n'+crypto[112:115]      
    parameter = {"sign_valid":sign_valid,"token":token_message}
    valid_key = requests.post(url="http://zlclclc.cn/exist_token",data = json.dumps(parameter))
    return token_message
