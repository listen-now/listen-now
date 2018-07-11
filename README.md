# Listen-now
![Python3.6.4](https://img.shields.io/badge/Python-3.6.4-green.svg)
![Listen-now](https://img.shields.io/badge/Listen--now-0.5.3-red.svg)

## 邮件列表
Listen-now开源项目公开的邮件列表地址为：listen-now-email@googlegroups.com
欢迎将你遇到的问题直接反馈到该地址。你的邮件将很快会得到回复。

## 版本升级历史

```
    * 0.1.0   上线网易云播放(搜索, id播放)
    * 0.2.0   上线QQ音乐、虾米音乐(搜索, id播放)
    * 0.3.0   上线README.md 详细说明, 启用Redis 一级缓存加快服务器响应
    * 0.5.0   上线测试终端版Listen-now(pymusic), 启用mongodb储存用户信息, 同步歌单
    * 0.5.1   优化后台响应, 启用异步IO设计, 启用代理ip设置
    * 0.5.3   终端版本支持单曲循环功能, 支持播放歌单, 支持随机播放热门歌曲(手气不错)

    * 下一个版本计划优化redis缓存设置, 防止出现缓存穿透、缓存雪崩情况

```
## 简要说明

这是一个能够解析三大(网易、虾米、QQ)音乐平台的Python脚本, 它可以被部署在服务器上, 接受post请求, 返回相应音乐的地址、歌词、演唱者等更多信息.
目前他提供两个版本，1. 部署于服务器上的后端API，2. 直接在terminal使用的终端听歌版本。

本项目在以下环境中编写并成功运行。
请注意，暂时不提供Windows版本。

```
Python 3.6.4
CentOS 7.0/Mac OS 10.13.4
Redis
uwsgi
Nginx
```

## 使用指南

[1. pymusic 使用指南](https://github.com/listen-now/listen-now/blob/master/README/pymusic-readme.md)

[2. API搭建版本](https://github.com/listen-now/listen-now/blob/master/README/API-readme.me)

[3. docker免配置版本](https://github.com/listen-now/listen-now/blob/master/README/docker-readme.me)

## 如何参与贡献？

[参与贡献指南](https://github.com/listen-now/listen-now/blob/master/CONTRIBUTING.md)




