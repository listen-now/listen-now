# Listen-now
这是一个能够解析三大(网易、虾米、QQ)音乐平台的Python程序, 它可以被部署在服务器上, 接受post请求, 返回相应音乐的地址、歌词、演唱者等更多信息.

## 快速开始

### 安装依赖环境
本项目在以下环境中编写并成功运行

```
Python 3.6.3
CentOS 7.0/Mac OS 10.13.4
Redis
Nginx
```

* 首先安装Python3, 并做好软连接(各种办法均可)

* 使用`pip3 install -r requirement.txt` 安装用到的外部库

* 使用`yum install redis`

* 可选启动redis及mongodb, 需要配置项目中的`setting.conf` 文件
    * 不启动相关数据库的话, 部分功能无法使用

* 整个免配置版本的正在准备docker, 后期你就可以直接下载体验, 它装好了所有环境并且使用Nginx和uwsgi来配置

### 测试
当完成上述配置后:

* 运行终端, 输入 `python3 main.py` 就可以尝试使用该脚本(启动后台flask)

* 接着再打开一个终端, 运行test_request.py 使用包括如下指令来在终端体验这个程序



### 一些说明
* setting.conf是用于维护用户使用的数据库/发送邮件模块的账户密码设置/flask开放的端口设置等

* 我们使用`Neteasymusic_song_maintain_db`中的爬虫, 来更新redis数据库中的网易云音乐歌曲id和音乐播放地址的对应关系, 以及各种热门歌单, 用户歌单同步等 

    * 接下来类似的更新音乐地址爬虫都会被部署

* 关于API接口反馈的状态码详细解释请查询SDK.md

* 为什么要维护redis, 为了降低服务器处理难度, 减小延迟.

* 用户的信息会被储存在mongodb, 用于同步用户歌单等信息

### 剩下没提到的文件是什么/用来做什么?
例如你看到的

* nginxzz.conf 是用来配置nginxzz反向代理的配置文件

* config.ini是用来配置uwsgi的

* access.log/error.log 是用来输出nginx的工作日志

* test_func文件是用来检测是否系统正常工作, 即单元测试文件和新功能的测试文件

* config.py是用来读入setting.conf文件中的配置信息, 用于系统初始化

* send_email.py正在开发, 他后期会用于用户注册的邮箱验证码发送, 紧急错误通知等等

* _config.yml是GitHub提供用于配置theme/主题的文件

* .gitignore是用来使Git忽略不需要上传的文件/类型

* LICENSE是开源声明文件.






