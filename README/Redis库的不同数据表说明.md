# Redis库的不同数据表说明

Redis库运用于系统一级缓存来协助服务器快速响应并处理数据

## 0号表
用于对应网易歌曲id和歌曲的播放地址
格式如下:

包括热门歌单, 热门歌曲, 热门排行榜
都是整理成id-play_url 方式
Key-Value 类型(Str)

* Key : NEM123456
* Value: http://music.163.com/song/media/outer/url?id=123456.mp3

## 1号表
1号库用于维护用户的热门歌单的地址、歌单封面、歌单名称
类型为:
    image_url:
    title:    
    song_list_url:

## 2号表
2号表用于维护虾米音乐的歌曲id和播放地址
格式如下:

包括热门歌单, 热门歌曲, 热门排行榜
都是整理成id-play_url 方式
Key-Value 类型(Str)

形式同0号表相似

## 3号表(计划中)
3号表用于维护登录用户的登录状态(cookies), 实现快速登录.


