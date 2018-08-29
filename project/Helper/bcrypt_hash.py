import bcrypt
import redis
from project.Config import config #从项目包顶导入
import copy
from project.Module import ReturnStatus
from project.Module import RetDataModule
import random, string
from pymongo import MongoClient
import execjs
import rsa
import time
import base64
from Crypto.Cipher import AES
from binascii import b2a_base64, a2b_base64
from cryptography.fernet import Fernet
from project.Config import config #从项目包顶导入


re_dict = copy.deepcopy(RetDataModule.mod_sign)

class AES_Crypt_Cookies(object):
    def __init__(self):
        self.mode = AES.MODE_CBC
        self.key  = self.Pad_Key(r"%s3(1LPJQEjszQIL")
        if int(config.getConfig("open_database", "redis")) == 1:
            host   = config.getConfig("database", "dbhost")
            port   = config.getConfig("database", "dbport")
            self.r = redis.Redis(host=host, port=int(port), decode_responses=True, db=6)  


    def Pad_Text(self, text, flag=1):
        if flag:
            text = bytes(text, encoding="utf8")
        while len(text) % 16 != 0:
            text += b'\0'
        return text

    def Pad_Key(self, key):
        key = bytes(key, encoding="utf8")
        while len(key) % 16 != 0:
            key += b'\0'
        return key
 
    def Creat_Token(self, timevalue, nickname, ip, ua):

        token_message = str(int(time.time()+timevalue*3600))+';'+nickname+';'+ip+';'+ua+';'+str(int(time.time()))
        texts = self.Pad_Text(token_message)
        aes = AES.new(self.key, self.mode,self.key)
        res = aes.encrypt(texts)

        Token = loginer()
        Token_Crypto            = Token.Creat_Return_Token(str(b2a_base64(res), encoding= "utf-8"))
        # print(str(Token_Crypto[0]))
        self.r.set(Token_Crypto[0], nickname)
        self.r.expire(Token_Crypto[0], 60)  
        # 生成预token
        # print(self.r.get(Token_Crypto[0]))

        re_dict["token_status"] = ReturnStatus.TOKEN_CREAT_SUCCESS
        return Token_Crypto
 
    def Decrypt_Check_Token(self,token_crypto, ip, ua):

        aes = AES.new(self.key, self.mode,self.key)
        # token_crypto = base64.b64decode(token_crypto)
        token_crypto = str(aes.decrypt(token_crypto), encoding="utf8").split(";")
        token_time   = int(token_crypto[0])
        now_time     = int(time.time())
        if now_time<token_time and ip == token_crypto[2] and ua == token_crypto[3]:
            print("[+]token is exist!")
            return 1
        else:
            print("[-]token bad!")
            return 0
        print(now_time, token_time, token_crypto)




class loginer(object):

    def __init__(self):

        if int(config.getConfig("open_database", "redis")) == 1:
            host         = config.getConfig("database", "dbhost")
            port         = config.getConfig("database", "dbport")
            self.r       = redis.Redis(host=host, port=int(port), decode_responses=True, db=4)
            # 四号表用于维护用户的密码盐值
            host         = config.getConfig("mongodb", "mongodbhost")
            port         = config.getConfig("mongodb", "mongodbport")            
            self.mong    = MongoClient(str(host), int(port))
            self.db      = self.mong.mydb
            self.user_db = self.db.User

    def Sign_Up_Encrypt(self, user_id, passwd="Wechat_Mini_Program"):
        global re_dict
        Token_Crypto = None
        if passwd == "Wechat_Mini_Program": # 注册请求来自微信则不验证密码信息
            if list(self.user_db.find({"user_id":user_id})) == []: # 还没注册
                self.user_db.insert({"user_id":user_id, "encrypt_passwd":"Wechat_Mini_Program"})
            re_dict["code"]    = ReturnStatus.USER_WECHAT_SIGN
            re_dict["status"]  = "Success"
            re_dict["user_id"] = user_id[::-1]
            create_token = AES_Crypt_Cookies()
            Token_Crypto = create_token.Creat_Token(timevalue, user_id[::-1], ip, ua)

        else: 
            user_id = user_id[::-1]
            if self.r.get(user_id) == None: # 如果redis查询结果为空，则证明账户可以注册
                salt   = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                passwd = (passwd + salt[:4])[::-1] + salt[4:]
                passwd = bytes(passwd, encoding = "utf8")
                hashed = bcrypt.hashpw(passwd, bcrypt.gensalt(10))
                # 对password做10轮的加密，获得了加密之后的字符串hashed，\
                # 生成形如：$2a$10$aoiufioadsifuaisodfuiaosdifasdf
                if list(self.user_db.find({"user_id":user_id})) == [] and self.r.set(user_id, salt) == True:
                    self.user_db.insert({"user_id":user_id, "encrypt_passwd":hashed})
                    re_dict["code"]    = ReturnStatus.USER_SIGN_SUCCESS
                    re_dict["status"]  = "Success"
                    re_dict["user_id"] = user_id[::-1]
                    create_token = AES_Crypt_Cookies()
                    Token_Crypto = create_token.Creat_Token(timevalue, user_id[::-1], ip, ua)
                    re_dict['token_message'] = Token_Crypto
                    # 返回token参数数据
            else:
                re_dict["code"]    = ReturnStatus.USER_SIGN_ERROR
                re_dict["status"]  = "Failed"
                re_dict["user_id"] = user_id[::-1]

        return re_dict

    def Creat_Return_Token(self, token_crypto):

        tag = bytes("NQZ",encoding="utf8")

        # with open('../project/Helper/pubkey.pem','r') as f:
        #     pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

        with open('../project/Helper/privkey.pem','r') as f:
            privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
        token_message = token_crypto
        # token_crypto = rsa.encrypt(token_message.encode(), pubkey)
        # 不进行公钥加密
        # 直接反馈加上标准内容的信息
        token_crypto = bytes(token_crypto, encoding='utf8') + tag
        signature = rsa.sign(token_message.encode(), privkey, 'SHA-1')
        print("token message encode = ", token_message.encode())
        # 利用私钥对信息进行签名
        signature = base64.encodestring(signature)
        return (token_crypto, signature)
        # 返回生成的token 和 sign 签名值

    def Check_Token(self, token_crypto, ip, ua):
        global re_dict
        if str(token_crypto)[-4:-1] != "NQZ":
            return "[-]token flag is error!"
        else:
            # with open('../project/Helper/privkey.pem','r') as f:
            #     privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

            token_message = base64.b64decode(token_crypto[:-4])

            # token_message = rsa.decrypt(token_crypto, privkey)
            print("RSA解密后 ", token_message)
            message       = AES_Crypt_Cookies()
            if message.Decrypt_Check_Token(token_message, ip, ua):
                # token 校验成功，合法
                re_dict["token_status"] = ReturnStatus.TOKEN_ERROR
            else:
                # token 校验失败，不合法
                re_dict["token_status"] = ReturnStatus.TOKEN_SUCCESS


    def Sign_In_Check(self, user_id, passwd="Wechat_Mini_Program"):
        global re_dict
        Token_Crypto = None

        if passwd == "Wechat_Mini_Program": # 证明输入的是微信的open_id，则不验证密码信息
            if list(self.user_db.find({"user_id":user_id})) == []: # 还没注册
                self.user_db.insert({"user_id":user_id, "encrypt_passwd":"Wechat_Mini_Program"})
            re_dict["code"]    = ReturnStatus.USER_WECHAT_SIGN
            re_dict["status"]  = "Success"
            re_dict["user_id"] = user_id[::-1]
            create_token = AES_Crypt_Cookies()
            Token_Crypto = create_token.Creat_Token(timevalue, user_id[::-1], ip, ua)
            re_dict["token_status"] = ReturnStatus.TOKEN_CREAT_SUCCESS
        else:
            user_id = user_id[::-1]
            if list(self.user_db.find({"user_id":user_id})) != [] and self.r.get(user_id) != None:
                salt   = self.r.get(user_id)
                passwd = bytes((passwd + salt[:4])[::-1] + salt[4:], encoding="utf8")
                hashed = list(self.user_db.find({"user_id":user_id}))[0]["encrypt_passwd"]
                if bcrypt.hashpw(passwd, hashed) == hashed:
                    print("Success!")
                    re_dict["code"]    = ReturnStatus.USER_SUCCESS_SIGN_IN
                    re_dict["status"]  = "Success"
                    re_dict["user_id"] = user_id[::-1]
                    create_token = AES_Crypt_Cookies()
                    Token_Crypto = create_token.Creat_Token(timevalue, user_id[::-1], ip, ua)
                    re_dict["token_status"] = ReturnStatus.TOKEN_CREAT_SUCCESS
                    re_dict['token_message'] = Token_Crypto
                    # 返回token参数以及token生成状态
                else:
                    print("Failed :(")
                    re_dict["code"]    = ReturnStatus.USER_FAILED_SIGN_IN
                    re_dict["status"]  = "Failed :("
                    re_dict["user_id"] = user_id[::-1]
            else:
                re_dict["code"]    = ReturnStatus.USER_NOT_SIGN_UP
                re_dict["status"]  = "Failed"
                re_dict["user_id"] = user_id[::-1]             

        return re_dict


if __name__ == '__main__':

    test = loginer()
    test.Sign_Up_Encrypt("passwde", "The powder toy")