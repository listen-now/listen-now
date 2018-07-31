from project.Module import RetDataModule
from project.Module import ReturnStatus
import redis
import copy
from project.Config import config

class Forbidden(object):

    def __init__(self):

        if int(config.getConfig("open_database", "redis")) == 1:
            host   = config.getConfig("database", "dbhost")
            port   = config.getConfig("database", "dbport")
            self.r = redis.Redis(host=host, port=int(port), decode_responses=True, db=7)  
            # 选择第7号表作为最近请求的token管理表，每一个key的有效期为1分钟
    
    def sign_ip(self, token):
        # 此处登记请求的token信息，key-value 字段.
        re_dict = copy.deepcopy(RetDataModule.mod_token)
        flag = self.r.get(token)
        if flag != None and flag<=40:
                flag += 1
                self.set(token, flag)    # 更新token 请求次数
                self.r.expire(token, 60) # 重新激活一分钟时效
                re_dict["code"] = ReturnStatus.TOKEN_SUCCESS
        elif flag == None:
            flag = 1
            self.set(token, flag)    # 更新token 请求次数
            self.r.expire(token, 60) # 重新激活一分钟时效
            re_dict["code"] = ReturnStatus.TOKEN_SUCCESS
        else:
            re_dict[""]

