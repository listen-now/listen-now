# Listen-now
这是一个能够解析三大(网易、虾米、QQ)音乐平台的Python程序, 它可以被部署在服务器上, 接受post请求, 返回相应音乐的地址、歌词、演唱者等更多信息.

##快速开始

###安装依赖环境
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

* 运行终端, 输入 `python3 neteasymusic.py` 就可以尝试使用该脚本







