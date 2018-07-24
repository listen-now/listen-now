# __fileName__ : ReturnStatus.py
# __date__ : 2018/07/04
# __author__ : Yaxuan, Cat.1
# __Update__ : 2018/07/19

SUCCESS              = 200 # 成功请求数据, 服务器处理成功
ERROR_METHOD         = 400 # 应该为POST请求却使用了GET请求
NO_MUSIC_DETAIL      = 401 # 该平台没有该歌曲
NO_EXISTS            = 402 # 没有该歌曲的更多结果啦
OVER_MAXPAGE         = 403 # 请求页数过大
ERROR_PARAMS         = 404 # 上传的参数不能被正确解析
ERROR_PSOT_DATA      = 405 # 请求的数据不是以json格式封装
NO_SUPPORT           = 406 # 目前不支持的音乐平台
ERROR_UNKNOWN        = 407 # 未知错误
DATABASE_OFF         = 408 # 未启用数据库, 却使用了依赖其的功能
NOT_SAFE             = 409 # 不安全的参数值要求
ERROR_SEVER          = 410 # 服务器内部错误或服务繁忙
USER_NOT_SIGN_UP     = 500 # 用户未注册
USER_SIGN_SUCCESS    = 501 # 用户注册成功
USER_SIGN_ERROR      = 502 # 用户名被注册过
USER_SUCCESS_SIGN_IN = 503 # 用户登录成功
USER_FAILED_SIGN_IN  = 504 # 用户登录失败
USER_WECHAT_SIGN     = 505 # 小程序注册/登录 成功
USER_WECHAT_ERROR    = 506 # 小程序注册/登录 发生未知错误
TOKEN_ERROR          = 100 # Token错误不合法或者预Token超时
TOKEN_SUCCESS        = 101 # 服务器验证Token成功
TOKEN_CREAT_SUCCESS  = 102 # 服务器生成Token成功
TOKEN_CREAT_FAILED   = 103 # 服务器生成Token遇到错误
TOKEN_IS_EXIST       = 104 # 预Token生成Token成功
