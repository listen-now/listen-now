import copy
import redis
from project.Config import config
from project.Module import RetDataModule
from project.Module import ReturnStatus

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
        try:flag=int(flag)
        except:flag=None
        print(flag)
        if flag != None and flag<=40:
                flag += 1
                self.r.set(token, flag)    # 更新token 请求次数
                self.r.expire(token, 60) # 重新激活一分钟时效
                re_dict["code"]   = ReturnStatus.TOKEN_SUCCESS
                re_dict["status"] = "TOKEN_SUCCESS"
        elif flag == None:
            flag = 1
            self.r.set(token, flag)    # 更新token 请求次数
            self.r.expire(token, 60) # 设置一分钟时效
            re_dict["code"]   = ReturnStatus.TOKEN_SUCCESS
            re_dict["status"] = "TOKEN_SUCCESS"
        elif flag>40:
            re_dict["code"]   = ReturnStatus.IP_FORBID
            re_dict["status"] = "IP_FORBID"
            flag += 1
            self.r.set(token, flag)    # 更新token 请求次数
            self.r.expire(token, 3600) # 重新激活一分钟时效

            # 设定ip封禁设置
        
        return re_dict

