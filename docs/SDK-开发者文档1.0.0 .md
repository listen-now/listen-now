[listen-now开发者文档说明]
=======================
### 版本 - 1.2.0
'''
该文件解释了Listen-now 前后端交互的使用说明
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
200 # 成功请求数据, 服务器处理成功
400 # 应该为POST请求却使用了GET请求
401 # 该平台没有该歌曲
402 # 没有该歌曲的更多结果啦
403 # 请求页数过大
404 # 传的参数不能被正确解析，或者缺失参数
405 # 请求的数据不是以json格式封装
406 # 目前不支持的音乐平台
407 # 未知错误
408 # 未启用数据库, 却使用了依赖其的功能
409 # 不安全的参数值要求
410 # 服务器内部错误
500 # 用户未注册
501 # 用户注册成功
502 # 用户名被注册过
503 # 用户登录成功
504 # 用户登录失败
505 # 小程序注册/登录 成功
506 # 小程序注册/登录 发生未知错误

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
  A         http://zlclclc.cn/search                    通过关键字搜索歌曲,后端会返回歌曲搜索详情，不包括播放地址，歌词，评论。开放网易，QQ，虾米
  B         http://zlclclc.cn/id                        通过id获取某一首歌曲的详细信息，包括播放地址，歌词，评论，发放网易，QQ，虾米
  C         http://zlclclc.cn/song_list_requests        通过歌单地址，歌单id来获取某一个歌单详情，目前开放了网易，QQ音乐，即将开发虾米
  D         http://zlclclc.cn/user_song_list            通过用户识别码[uid/uin]获取用户详情，目前开放网易，QQ音乐
```
通用参数说明:
-----------
```
platform 请求音乐平台，目前提供如下：
    。Neteasymusic
    。Xiamimusic
    。QQmusic

token 服务器加密参数，请求任何API均需要提供：

```

API请求说明详情:
--------------

* API [A]
>请求地址:
```
http://zlclclc.cn/search
```
>请求参数说明:
```
参数          可选                      描述
title       否     关键字，主要的内容是歌手名/歌曲名，例如:纸短情长，张学友
platform    否     音乐平台，为通用参数platform列出字段
page        是     搜索页，不加入该参数默认返回第一页10首，通过增加page来改变搜索信息  
token       否     token参数
```
>请求示例:
```
{
    "title":"成都",
    "token":"your_token_message_content",
    "platform":"Neteasymusic"
}
```
                    
        
* API [B]
>请求地址: 
```
http://zlclclc.cn/id
```
>请求参数说明:
```
参数          可选    描述
id            否     歌曲识别码，各平台的歌曲识别码格式不一样，需要请求获取
platform      否     音乐平台，通用参数
token         否     token参数
```
>请求示例:
```
{
    "id":"0015H75B1NvYzl",
    "platform":"QQmusic",
    "token":"your_token_message_content"
}
```
* API [C]
>请求地址:
```
http://zlclclc.cn/song_list_requests
```
>请求参数说明:
```
参数        可选      描述
url         否       歌单地址，目前只支持网易，QQ
platform    否       音乐平台，通用参数
token       否       token参数

```


* API [D]
>请求地址:
```
http://zlclclc.cn/user_song_list
```
>请求参数说明:
```
参数        可选        描述
uid         否       用户识别码，目前只支持网易，QQ
platform    否       确认用户同步的平台选择
token       否       token参数

```

成功请求
-------
* 请求示例:
```
{
    "title":"纸短情长",
    “platform”:”Neteasymusic”,
    “page”: 1,
    "token":"your_token_message_content"
}
```
* 返回值:
```
{
    "song": {
      "totalnum": 10,
      "list": [
          {
          "image_url": "http://p1.music.126.net/tbZaE-DjL_BkemynFlL1cQ==/109951163052534918.jpg",
          "music_name": "纸短情长（完整版）",
          "artists": "烟把儿",
          "play_url": "http://music.163.com/song/media/outer/url?id=516076896.mp3",
          "music_id": 516076896,
          "lyric": "[00:00.00] 作曲 : 言寺\n[00:01.00] 作词 : 言寺\n[00:26.290]你陪我步入蝉夏"
          },
          {
          "music_id": 429459947,
          "play_url": "http://music.163.com/song/media/outer/url?id=429459947.mp3",
          "artists": "烟把儿",
          "music_name": "纸短情长"
          },
          {
          "music_id": 557581284,
          "play_url": "http://music.163.com/song/media/outer/url?id=557581284.mp3",
          "artists": "花粥",
          "music_name": "纸短情长"
          },
          {
          "music_id": 560899696,
          "play_url": "http://music.163.com/song/media/outer/url?id=560899696.mp3",
          "artists": "仇志",
          "music_name": "纸短情长"
          },
          {
          "music_id": 547607305,
          "play_url": "http://music.163.com/song/media/outer/url?id=547607305.mp3",
          "artists": "尚士达",
          "music_name": "纸短情长（Cover：烟把儿）"
          },
          {
          "music_id": 505080482,
          "play_url": "http://music.163.com/song/media/outer/url?id=505080482.mp3",
          "artists": "烟把儿",
          "music_name": "纸短情长（试听版）"
          },
          {
          "music_id": 557583297,
          "play_url": "http://music.163.com/song/media/outer/url?id=557583297.mp3",
          "artists": "花粥",
          "music_name": "纸短情长 - 伴奏"
          },
          {
          "music_id": 573228935,
          "play_url": "http://music.163.com/song/media/outer/url?id=573228935.mp3",
          "artists": "黄昌奕",
          "music_name": "纸短情长（原唱：烟把儿）"
          },
          {
          "music_id": 556030014,
          "play_url": "http://music.163.com/song/media/outer/url?id=556030014.mp3",
          "artists": "小马",
          "music_name": "纸短情长"
          },
          {
          "music_id": 543634002,
          "play_url": "http://music.163.com/song/media/outer/url?id=543634002.mp3",
          "artists": "烟把儿",
          "music_name": "纸短情长酒桌版"
          }
      ]
    },
    "code": "200",
    "status": "Success",
    "now_page": 1,
    "next_page": 2,
    "before_page": 0
}
```
