# __fileName__ : ReturnStatus.py
# __date__ : 2018/07/04
# __author__ : Yaxuan

SUCCESS = 200 #成功请求数据, 服务器处理成功
ERROR_METHOD = 400 #应该为POST请求却使用了GET请求
NO_EXISTS = 402 #没有该歌曲的更多结果啦
OVER_MAXPAGE = 403 #请求页数过大
ERROR_PARAMS = 404 #传的参数不能被正确解析
ERROR_PSOT_DATA = 405 #请求的数据不是以json格式封装
NO_SUPPORT = 406 #目前不支持的音乐平台
ERROR_UNKNOWN = 407 #未知错误
DATABASE_OFF = 408 #未启用数据库, 却使用了依赖其的功能
NOT_SAFE = 409 #不安全的参数值要求
ERROR_SEVER = 410 #服务器内部错误