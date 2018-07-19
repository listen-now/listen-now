import bcrypt
import redis
from project.Config import config #从项目包顶导入
import copy
from project.Module import ReturnStatus
from project.Module import RetDataModule
import random, string
from pymongo import MongoClient

re_dict = copy.deepcopy(RetDataModule.mod_sign)

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
        if passwd == "Wechat_Mini_Program": # 注册请求来自微信则不验证密码信息
            if list(self.user_db.find({"user_id":user_id})) == []: # 还没注册
                self.user_db.insert({"user_id":user_id, "encrypt_passwd":"Wechat_Mini_Program"})
            re_dict["code"]    = ReturnStatus.USER_WECHAT_SIGN
            re_dict["status"]  = "Success"
            re_dict["user_id"] = user_id[::-1]
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
            else:
                re_dict["code"]    = ReturnStatus.USER_SIGN_ERROR
                re_dict["status"]  = "Failed"
                re_dict["user_id"] = user_id[::-1]

        return re_dict


    def Sign_In_Check(self, user_id, passwd="Wechat_Mini_Program"):
        global re_dict
        if passwd == "Wechat_Mini_Program": # 证明输入的是微信的open_id，则不验证密码信息
            if list(self.user_db.find({"user_id":user_id})) == []: # 还没注册
                self.user_db.insert({"user_id":user_id, "encrypt_passwd":"Wechat_Mini_Program"})
            re_dict["code"]    = ReturnStatus.USER_WECHAT_SIGN
            re_dict["status"]  = "Success"
            re_dict["user_id"] = user_id[::-1]
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