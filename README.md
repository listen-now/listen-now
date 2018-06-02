# Listen-now
当前版本 - 0.0.3.1
版本升级历史

```
    * 0.0.1 上线网易云播放(搜索, id播放)
    * 0.0.2 上线QQ音乐、虾米音乐(搜索, id播放)
    * 0.0.2.1 上线README.md 详细说明, 启用Redis 一级缓存加快服务器响应
    * 0.0.2.2 上线测试终端版Listen-now(pymusic), 启用mongodb储存用户信息, 同步歌单
    * 0.0.3.1 优化后台响应, 启用异步IO设计

```
## 简要说明
这是一个能够解析三大(网易、虾米、QQ)音乐平台的Python程序, 它可以被部署在服务器上, 接受post请求, 返回相应音乐的地址、歌词、演唱者等更多信息.

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

* 首先安装Python3, 并做好软连接(各种办法均可)

* 使用`pip3 install -r requirement.txt` 安装用到的外部库

* 使用`yum install redis`

* 使用`yum install mongodb`

* 可选启动redis及mongodb, 需要自行配置项目中的`setting.conf` 文件
    * 不启动相关数据库的话, 部分功能无法使用!

* 整个免配置docker版本正在准备, 后期你就可以直接下载体验, 它装好了所有环境并且使用Nginx和uwsgi来配置, 而不是使用flask的debug模块

### 测试
如果觉得麻烦? 请直接修改setting.conf中的xx参数为1, 再按下面的操作即可

当完成上述配置后:


* 运行终端, 输入 `python3 main.py` 就可以尝试使用该脚本(启动后台flask)

* 接着再打开一个终端, 输入`python3 set_init_.py` 当反馈`[+]终端命令初始化成功!`后你就可以使用下面的命令来使用后台服务
    

```
# pymusic -h(显示所有的帮助信息)
```    
```
usage: pymusic [-h] [-t TITLE] [-p PLATFORM] [-id ID] [-n NUM] [-page PAGE]

optional arguments:
  -h, --help   show this help message and exit
  
  -t TITLE       like: 白金迪斯科
  -p PLATFOR     like: 网易(net)/QQ(qq)/虾米(xia)
  -id ID,        like 123456
  -n NUM,        like 1
  -page PAGE     like 1

```
    
    # pymusic -t(歌曲名字)  -p(歌曲平台)

     pymusic -t 纸短情长 -p net
    

```    0    纸短情长（完整版）    烟把儿
1    纸短情长    烟把儿
2    纸短情长    花粥
3    纸短情长    仇志
4    纸短情长（Cover 烟把儿）    杨舒怀
5    纸短情长（Cover 烟把儿）    萧忆情Alex
6    纸短情长（Cover：烟把儿）    冯心怡
7    纸短情长（Cover：烟把儿）    尚士达
8    纸短情长（Cover 烟把儿）    叶洛洛
9    纸短情长（试听版）    烟把儿
10    >>>Enter your select 

```
    * 键入w来上翻一页, s为下翻一页被选歌曲
    * 键入歌曲前面的序号来播放歌曲
    * -p 目前可选如下 net/网易、qq(QQ音乐)、xia(虾米音乐)

如果你有歌曲id, 可直接准确播放歌曲

```
# pymusic -id 123456 -p net
```    

如果你选了一首不喜欢的歌曲, 请直接使用Ctrl + c 来选择输入检索新歌曲



### 一些说明
* setting.conf是用于维护用户使用的数据库/发送邮件模块的账户密码设置/flask开放的端口设置等

* 我们使用`Neteasymusic_song_maintain_db`中的爬虫, 来更新redis数据库中的网易云音乐歌曲id和音乐播放地址的对应关系, 以及各种热门歌单, 用户歌单同步等 

    * 接下来类似的更新音乐地址爬虫都会被部署

* 关于API接口反馈的状态码详细解释请查询SDK.md

* 为什么要维护redis, 为了降低服务器处理难度, 减小延迟.

* 用户的信息会被储存在mongodb, 用于同步用户歌单等信息

### 剩下没提到的文件是什么/用来做什么?
* 如果初始化set_init.py反馈
    `ln: /xxx/bin/pymusic:        File exists`
    则可能出现了您重复初始化/该(pymusic)您已经占用.
    
    可以使用 `sudo rm /xxx/bin/pymusic` 再次初始化, 当初始化成功后您就可以使用pymusic -h 来测试程序是否可用
    
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






