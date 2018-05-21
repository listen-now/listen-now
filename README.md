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

* 启动redis, 并配置项目中的`setting.conf` 文件

### 测试
当完成上述配置后:

* 运行终端, 输入 `python3 neteasymusic.py` 就可以尝试使用该脚本

### 一些说明

* 我们使用`Neteasymusic_ Redis_SongStatus.py`脚本爬虫, 来更新redis数据库中的网易云音乐歌曲id和音乐播放地址的对应关系

* 接下来类似的更新音乐地址爬虫都会被部署

* 关于API接口反馈的状态码详细解释请查询SDK.md

* 为什么要维护redis, 为了降低服务器处理难度, 减小延迟.

### 剩下没用到的文件是什么?
例如你看到的

* nginxzz.conf 是用来配置nginxzz反向代理的配置文件

* config.ini是用来配置uwsgi的

* access.log/error.log 是用来输出nginx的日志

* test_api.py是用来检测是否系统正常工作(向服务器发送post请求, 并打印输出)







