# Listen-now
[](https://img.shields.io/badge/Python-3.6.4-green.svg)
[](https://img.shields.io/badge/Listen--now-0.5.2-red.svg)
版本升级历史

```
    * 0.0.1   上线网易云播放(搜索, id播放)
    * 0.0.2   上线QQ音乐、虾米音乐(搜索, id播放)
    * 0.0.3   上线README.md 详细说明, 启用Redis 一级缓存加快服务器响应
    * 0.0.5   上线测试终端版Listen-now(pymusic), 启用mongodb储存用户信息, 同步歌单
    * 0.0.5.1 优化后台响应, 启用异步IO设计, 启用代理ip设置
    * 0.0.5.2 终端版本支持单曲循环功能, 支持播放歌单, 支持随机播放热门歌曲(手气不错)

    * 下一个版本计划优化redis缓存设置, 防止出现缓存穿透、缓存雪崩情况

```
## 简要说明
这是一个能够解析三大(网易、虾米、QQ)音乐平台的Python脚本, 它可以被部署在服务器上, 接受post请求, 返回相应音乐的地址、歌词、演唱者等更多信息.
目前他提供两个版本，1.部署于服务器上的后端API，直接在terminal使用的终端听歌版本。

## 快速开始!

### 安装依赖环境
本项目在以下环境中编写并成功运行

```
Python 3.6.3
CentOS 7.0/Mac OS 10.13.4
Redis
uwsgi
Nginx
```

1.[pymusic（terminal听歌) 使用](https://github.com/listen-now/listen-now/blob/master/pymusic-readme.md)

2.[API搭建版本](https://github.com/listen-now/listen-now/blob/master/API-readme.md)

3.[docker免配置版本](https://github.com/listen-now/listen-now/blob/master/docker-readme.md)




### 文件说明
* setting.conf是用于维护用户使用的数据库/发送邮件模块的账户密码设置/flask开放的端口设置等

* 我们使用`Neteasymusic_song_maintain_db`中的爬虫, 来更新redis数据库中的网易云音乐歌曲id和音乐播放地址的对应关系, 以及各种热门歌单, 用户歌单同步等 

    * 接下来类似的更新音乐地址爬虫都会被部署

* 关于API接口反馈的状态码详细解释请查询SDK.md

* 为什么要维护redis, 为了降低服务器处理难度, 减小延迟.

* 用户的信息会被储存在mongodb, 用于同步用户歌单等信息

### 剩下没提到的文件是什么/用来做什么?
* 如果初始化setup.py反馈
    `ln: /xxx/bin/pymusic:        File exists`
    则可能出现了您重复初始化/该(pymusic)您已经占用.
    
    可以使用指令 `sudo rm /xxx/bin/pymusic`后, 再次初始化, 当初始化成功后您就可以使用pymusic -h 来测试程序是否可用
    
其他例如你看到的

* nginxzz.conf 是用来配置nginxzz反向代理的配置文件(原谅这个命名)

* config.ini是用来配置uwsgi的

* access.log/error.log 是用来输出nginx的工作日志

* test_func文件是用来检测是否系统正常工作, 即单元测试文件和新功能的测试文件

* config.py是用来读入setting.conf文件中的配置信息, 用于系统初始化

* send_email.py正在开发, 他后期会用于用户注册的邮箱验证码发送, 紧急错误通知等等

* _config.yml是GitHub提供用于配置theme/主题的文件

* .gitignore是用来使Git忽略不需要上传的文件/类型

* LICENSE是开源声明文件.






