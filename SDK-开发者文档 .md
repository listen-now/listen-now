#SDK-开发者文档 
###版本 - 0.0.2.2
'''
本文标注了目前该小程序前后端交互的
状态解读
和开发指南
'''

##status-状态码信息
###400
##### 原因: 应该为POST请求却使用了GET请求

1.返回示例:
`{"code":"400", "status":"Failed"}`

2.错误请求示例
无

###401
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
###402
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


###403
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

###404
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

###405
##### 原因: 请求的数据不是以json格式封装

1.返回示例:
`{"code":"405", "status":"Failed", 
"detail":"post not json_data!"}`

2.错误请求示例

```
  title="成都"&platform="Neteasymusic"
```
###406
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
###408
##### 原因: 未启用数据库, 却使用了依赖其的功能

1.返回示例:
`{"code":"408", "status":"Failed", 
"detail":"数据库未启用"`



###200
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

##200正确状态码返回的数据解读
###网易云音乐

以以下请求为例:

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
	'status': 'Success'
}
```






