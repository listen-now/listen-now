[listen-now开发者文档说明]
=======================
### 文档支持版本 - 1.5.3
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
提交主机地址：https://www.zlclclc.cn/ (目前测试服务，暂时不启用SSL加密)
或者        http://zlclclc.cn
测试服务器地址：http://118.126.93.123
```

# @API接口地址
```
  查询索引      接口地址                                                  描述
  A         http://zlclclc.cn/search                    通过关键字搜索歌曲,后端会返回歌曲搜索详情，不包括播放地址，歌词，评论。开放网易，QQ，酷狗，酷我，百度，咪咕
  B         http://zlclclc.cn/id                        通过id获取某一首歌曲的详细信息，包括播放地址，歌词，评论，开放网易，QQ，酷狗，酷我，百度，咪咕
  C         http://zlclclc.cn/song_list_requests        通过歌单地址，歌单id来获取某一个歌单详情，目前开放了酷狗，网易，虾米
  D         http://zlclclc.cn/TopSongList               通过GET/POST请求返回21个热门歌单数据
  E         http://zlclclc.cn/user_song_list            用户个人歌单同步，返回个人所有歌单，目前提供网易和QQ
```
通用参数说明:
-----------
```
platform 请求音乐平台参数，目前提供如下选择：
    。Neteasymusic
    。Xiamimusic
    。QQmusic
    。Kugoumusic
    。Kuwomusic
    。Baidumusic
    。Migumusic

token 服务器加密参数，请求任何API均需要提供：
具体请参考 `token参数请求说明` 。

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
```
>请求示例:
```
{
    "title":"成都",
    "platform":"Neteasymusic"
}
```
       
>返回示例:
```

{
    'code' : 200,
    'status' : 'Success',
    'now_page' : 1,
    'next_page' : 2,
    'before_page' : 0,
    'song': {
        'totalnum' : 1,
        'list' : [
                    {
                      "music_name":"浮夸",
                      "artists":"陈奕迅",
                      "id":"xsc124sq"
                    }
                    ...
                  ] 
        }
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
id            否     歌曲识别码，各平台的歌曲识别码格式不一样，需要请求search API获取
platform      否     音乐平台，通用参数
```
>请求示例:
```
{
    "id":"0015H75B1NvYzl",
    "platform":"QQmusic",
}
```
>返回示例:
```

{
    'code' : 200,
    'status' : 'Success',
    'play_url' : 'http://music.163.com/song/media/outer/url?id=64886.mp3',
    'music_id' : '64886',
    'music_name' : '浮夸',
    'artists' : '陈奕迅',
    'image_url' : 'http://p1.music.126.net/q4MZj15xz1usJq0dIu-LRg==/109951163381539466.jpg',
    'lyric' : '[by:有誰而過]\n[00:00.00] 作曲 : C. Y. Kong\n[00:01.00] 作词 : 黄伟文\n[00:29.22]有人问我 我就会讲\n[00:32.53]但是无人来\n...',
    'tlyric':'null',
    'comment':[        
                {
                  "comment_time": "2015--05--19 15:34:00",
                  "comment_content": "听这首歌产生共鸣，可能是因为我就像歌中的喽啰，出身于农村，毕业于三本，无钱无势无背景，感觉自己就像是人潮内不被理睬的那一个，我夸张，我害怕，想找到一个属于自己的木村，今年凭着自己的努力和运气考上了家里的农商行，虽不耀眼但也算体面的工作，幸运儿并不多，我只是用十倍苦心做突出一个，，",
                  "likecount": 68261,
                  "username": "1siyinyue"
                },
                ...
              ]
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
id          否       歌单id，目前只支持网易，QQ，酷狗
platform    否       音乐平台，通用参数
page        否       歌单中的页数，每页返回小于等于30首音乐
```

>请求示例:
```
{
    "id":"524599",
    "platform":"Kugoumusic",
    "page":1
}
```


>返回示例:
```

{
    'code' : 200,
    'status' : 'Success',
    'dissid' : '524599',
    'dissname' : '有没有那么一首歌，让你愿意跟着一起和',
    'nickname' : 'Layis-eo',
    'info':'看一场演唱会最难忘的除了能够亲眼看到自己的偶像之外，和上万个同好者一起大声大合唱也会成为人生中最美好的回忆之一。\n\n所以相比于录音室版本，有时候我更加青睐听演唱会live版...',
    'image_url':'http://imge.kugou.com/soft/collection/400/20180904/20180904094205591103.jpg',
    'song' : {
        'totalnum' : 9,
        'curnum' : 9,
        'list' : [            
                    {
                      "music_name": "张惠妹 - 我可以抱你吗 (Live)",
                      "artists": "张惠妹 ",
                      "id": "16BD201392E5A03934F016EA3A133BD5"
                    },
                    ...
                ]
        }
} 
```



* API [D]
>请求地址:
```
http://zlclclc.cn/TopSongList

```
>请求参数说明:
```
参数        可选        描述
无
```
>请求示例:
```
暂时仅提供GET请求，返回的歌单数据均为Kugoumusic，在请求详细歌单时，请将平台写为Kugoumusic
```

>返回示例:
```

{
    'code' : 200,
    'status' : 'Success',
    'totalitem' : 21,
    'itemlist' : [
                    {
                      'item_id' : '524599',
                      'item_name' : '有没有那么一首歌，让你愿意跟着一起和',
                      'item_desc' : '看一场演唱会最难忘的除了能够亲眼看到自己的偶像之外，和上万个同好者一起大声大合唱也会成为人生中最美好的回忆之一。\n\n所以相比于录音室版本，有时候我更加青睐听演唱会live版，在live版里我们能够感受到歌手们情到深处的悲伤...',
                      'image_url' : 'http://imge.kugou.com/soft/collection/400/20180904/20180904094205591103.jpg',
                     },
                     ...
            ]
} 
```


* API [E]
>请求地址:
```
http://zlclclc.cn/user_song_list
```
>请求参数说明:
```
参数        可选        描述
uid         否       用户识别码，目前只支持网易，QQ
platform    否       确认用户同步的平台选择

```



