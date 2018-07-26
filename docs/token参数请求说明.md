# 关于token请求参数的简单说明

[listen-now开发者文档说明之token参数]
=======================
### 版本 - 1.2.0
'''
该文件解释了Listen-now 前后端交互使用的token参数请求说明
和状态码的解读
以及开发指南
'''

# @状态码说明
```
100 # Token错误不合法或者预Token超时
101 # 服务器验证Token成功
102 # 服务器生成Token成功
103 # 服务器生成Token遇到错误
104 # 预Token生成Token成功

```

# @请求方式说明
```
暂时提供POST、GET方式请求
以raw格式进行数据提交
提交主机地址：https://www.zlclclc.cn/
或者        http://zlclclc.cn
测试服务器地址：http://118.126.93.123
```

# @API接口地址
```
  查询索引      接口地址                                                  描述
  A         https://www.zlclclc.cn/get_token                 通过GET/POST请求获得预token，用于前端验证
  B         https://www.zlclclc.cn/exist_token               验证预token无误后请求该地址得到长效token

```
通用参数说明:
-----------
```
暂无

```

使用说明:
-----------
```
为了获得可用的token，你首先需要请求API接口A，得到服务器发放的预token，这个token只有一分钟的时效，你需要在一分钟内通过之前早已发放的
RSA公钥验证随接口返回的签名有效性；验证签名后，请求API接口B去使预token生成长效token（目前有效期为2天），或者签名不正确的话，接口B会返回
新的预token用于验签。

当你的预token成功注册为token后请将其加入到Headers 里的Authorization字段，同时在请求服务器任何API的时候都带上"token"参数，服务器会随机
抽取该两个参数/字段中任意一个用于检测，同时你需要维护cookies中该内容不受影响，cookies中token参数仍会被服务器随机抽取验证参数是否合法

```

API请求说明详情:
--------------

* API [A]
>请求地址:
```
http://zlclclc.cn/get_token
```
>请求参数说明:
```
参数          可选                        描述
user_id       否     用户在平台上的用户名，微信端为open_id，web端为注册的用户user_id

当用户是登录时，必须以post方式请求该地址提交user_id参数得到该用户的预token；
而访客听歌亦需要token，此种情况只需要以GET方式请求该地址得到默认用户的预token。

```
>请求示例:
```
{
    "user_id":"Listen-now-user"
}
```

* API [B]
>请求地址:
```
http://zlclclc.cn/exist_token
```
>请求参数说明:
```
参数              可选                        描述
sign_valid(int)   否     本地验证签名是否有效，有效返回1，无效返回0，返回无效的话会将发放新的预token
token(str)        否     发放的预token，验证签名通过后重新回传
user_id(str)      是     用户是登录状态请求token时（即请求get_token地址时为post请求的）必须提供user_id/open_id否则不需要，系统将提供默认用户名

```
>请求示例:
```
{
    "sign_valid":1,
    "token":"your_token_message_content",
    "user_id":"Listen-now-user"
}

