# SDK-开发者文档 
### 版本 - 0.5.3
目前后端版本 0.5.3
'''
该文件解释了Listen-now 前后端交互的使用说明
和状态码的解读
以及开发指南
'''
## 目前可用的请求API 解释

### Search API
说明：用于请求后台系统搜索某首歌或者某一位歌手，每次系统默认返回10首音乐，为了获得之后的音乐可以增加page参数请求。

请求方式：

    通过POST方法发送JSON请求到
    http://zlclclc.cn/search
    

**目前开放的请求参数：**

* **title** 

    主要的内容是歌手名/歌曲名
* **platform**

    请求的音乐平台标示，
    目前参数有如下：
    * `Neteasymusic`
    * `Xiamimusic`
    * `QQmusic`
* **page**(可选)
    
    不加入该参数请求默认返回10首第一页的音乐信息。
    
    该参数用于请求搜索页的不同页的音乐信息，每一页会返回10首歌曲

### ID_request API
说明：用于请求后台系统搜索某一个有确认音乐ID的音乐的详细信息，包括专辑图片，歌词信息。

请求方式：

    通过POST方法发送JSON请求到
    http://zlclclc.cn/id
    

**目前开放的请求参数：**

* **id（请求网易和虾米时用到）** 

    当请求网易和虾米时，请使用歌曲的精确id识别码来获得某一首歌的详细信息。

* **media_mid 和 songmid（请求QQ音乐时用到）** 

当请求的平台是QQ音乐时，QQ音乐的歌曲唯一标示码为这两个参数，请添加这两个参数然后请求后端。

* **platform**

    请求的音乐平台标示，
    目前参数有如下：
    * `Neteasymusic`
    * `Xiamimusic`
    * `QQmusic`

### Return_User_Song_List_Detail API

说明：用于向前端返回某一个歌单的详细信息(包括 歌单的名称，歌单id，每首歌曲id，歌曲名称，歌曲演唱者)，目前只开放了网易查询。

请求方式：

    通过POST方法发送JSON请求到
    http://zlclclc.cn/song_list_requests
    

**目前开放的请求参数：**

* **url** 

    目前只启用了网易歌单搜索功能，所以你直接请求url即可，这个url就是你想要知道的歌单的url。
    
    
### Return_User_Song_List API
说明：用于请求后台系统搜索某一一位用户的详细信息，包括该用户的所有歌单信息，目前只开放了网易用户查询。

请求方式：

    通过POST方法发送JSON请求到
    http://zlclclc.cn/user_song_list
    

**目前开放的请求参数：**

* **uid** 

    用户的网易用户名识别码，一般是一串数字，例如123456，标示该用户。


## status-状态码信息解读
### 400
##### 原因: 应该为POST请求却使用了GET请求

1.返回示例:
`{"code":"400", "status":"Failed"}`

2.错误请求示例
无

### 401
##### 原因: 该音乐平台没有该歌曲(一般考虑是用户输入错误)

1.返回示例:
`{"code":"401", "status":"Failed", 
"detail":"post not json_data!"}`

2.错误请求示例

```
{
  "title":"random.randchar()",
  "platform":"Neteasymusic"
}
```
### 402
##### 原因: 没有该歌曲的更多结果啦

1.返回示例:
`{"code":"402", "status":"Failed", 
"detail":"Is so many response!"}
`

2.错误请求示例

```
{
  "title":"成都",
  "platform":"Neteasymusic"
  "page":12
}
```
目前最大支持100首搜索(网易接口不允许更大的请求)
也就是前十页


### 403
##### 原因: 请求页数过大

1.返回示例:
`{"code":"403", "status":"Failed",
     "detail": "Is so many response!",
}`

2.错误请求示例

```
{
  "title":"成都",
  "platform":"Neteasymusic"
}
```

### 404
##### 原因: 上传的参数不能被正确解析

1.返回示例:
`{"code":"404", "status":"Failed"}
`

2.错误请求示例

```
{
  "title":"%¥&*(&(*&--!0",
  "platform":"Neteasymusic",
  "page":12
}
```

### 405
##### 原因: 请求的数据不是以json格式封装

1.返回示例:
`{"code":"405", "status":"Failed", 
"detail":"post not json_data!"}`

2.错误请求示例

```
  title="成都"&platform="Neteasymusic"
```
### 406
##### 原因: 目前不支持的音乐平台

1.返回示例:
`{"code":"406", "status":"Failed", 
"detail":"Not know platform!"`

2.错误请求示例

```
{
  "title":"成都",
  "platform":"Apple Music"
}
```
### 408
##### 原因: 未启用数据库, 却使用了依赖其的功能

1.返回示例:
`{"code":"408", "status":"Failed", 
"detail":"数据库未启用"`



### 200
##### 原因: 成功请求数据, 服务器处理成功

1.返回示例:
`{"code":"200", "status":"Success"}`

2.正确请求示例

```
{
  "title":"成都",
  "platform":"Neteasymusic"
}
```

----------

## 200正确状态码返回的数据解读
### 网易云音乐

使用 以下请求为例:

```
{
  "title":"成都",
  "platform":"Neteasymusic",
  "page":1
}
```

服务器将会返回以下内容:

###虾米音乐
以以下请求为例:

```
{
  "title":"成都",
  "platform":"Xiamimusic",
  "page":1
}
```

服务器将会返回以下内容:

```{
	'0': {
		'play_url': 'http://m128.xiami.net/
326/76326/2102413795/1792702528_14849658
14706.mp3?
auth_key=1526612400-0-0-9f0ea69a015dfd8f
f8c7699009933813',

		'music_id': 1792702528,
		// 备选歌曲1的歌曲id
		'music_name': '成都',
		// 备选歌曲1的歌曲名
		'artists': '赵雷',
		// 备选歌曲1的演唱者
		'image_url': 'http://pic.xiami.net/images/album/
img87/181/585a3226db20e_9076087_14823060
86_1.jpg',
    // 备选歌曲1的专辑封面
		'lyric': '[00:03.863]作曲：赵雷
		\n[00:05.463]编曲：赵雷 / 喜子
		\n[00:18.105]让我掉下眼泪的
		\n[00:21.737]不止昨夜的酒\n...
		[04:21.013]走过小酒馆的门口
		\n[04:35.516]和我在成都的街头走一走
		\n[04:43.062]直到所有的灯都熄灭了也不停留'
	},
	// 备选歌曲1的歌词
	
	'1': {
		'music_id': 1795553923,
      // 备选歌曲2的歌曲id
		'music_name': '成都（Cover）',
		// 备选歌曲2的歌曲名称
		'artists': '阿金和玄子',
		// 备选歌曲2的演唱者
		'image_url': 'http://pic.xiami.net/images/album/img53/133583753/5182221487518222_1.jpg'
		// 备选歌曲2的专辑图片
	},
 //	...一直到十为止
	'10': {
		'music_id': 1802877183,
		'music_name': '成都',
		'artists': '曲肖冰',
		'image_url': 'http://pic.xiami.net/images/album/img33/110/5acc77add4aac_5518133_1523349421_1.jpg'
	},
	// 下面是状态码信息
	'code': '200',
	'status': 'Success',
  'now_page': 1,
  'next_page': 2,
  'before_page': 0
}

code就是状态码信息，不论是否请求成功都
会返回一个状态信息，请根据上面写的状态
信息解读来理解请求状况。

status是对于状态信息的简单解读，可能为空。

now_page，next_page，before_page
是为了方便前端请求歌曲下一页，上一页而
返回的数据。
```




