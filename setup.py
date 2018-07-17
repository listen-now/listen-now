#!/usr/bin/env python3
# @File:set_init.py
# @Date:FileDate
# Author:Cat.1

import os
import sys
import platform

path1 = "sudo ln -s " + os.path.abspath('.') + "/Pymusic/music.py " + "/usr/local/bin/pymusic" 
path2 = "sudo ln -s " + os.path.abspath('.') + "/Pymusic/read_lyric.py " + "/usr/local/bin/read_lyric" 

try:
    os.system(path1)
    os.system(path2)
except:
    print("[-]请手动初始化终端命令功能")
    print("参考指令 -> " + path2)
    print("参考指令 -> " + path1)
else:
    print("[+]终端命令初始化成功!")

try:
    platform = sys.platform
except:
    print("识别操作系统时发现未知错误")
else:
    if platform == "darwin":
        os.system("brew install mpg123")
        os.system("brew install ffmpeg")
    elif platform == "linux":
        platform = {"1":"基于Redhat的发行版及centos", "2":"debian及基于debian的发行版"}
        platform = platform[input("请选择你的linux版本\n1.)基于Redhat的发行版及centos\n2.)debian及基于debian的发行版\n->")]
        if platform == "基于Redhat的发行版及centos":
            os.system("sudo yum install mpg123")
            os.system("sudo yum install ffmpeg")
        elif platform == "debian及基于debian的发行版": 
            os.system("sudo apt-get install mpg123")
            os.system("sudo apt-get install ffmpeg")
    else:
        print("暂时不支持Win平台")

# 关于判断用户的Python版本中pip的构建问题
pip = {"1":"pip", "2":"pip3", "3":"other"}
pip = pip[input("请选择你的pip管理工具使用的哪一个名称\n1.)pip\n2.)pip3\n3.)other\n->")]
if pip == "pip3":
    os.system("pip3 install --upgrade pip")
    os.system("pip3 install -r requirements.txt")
elif pip == "pip":
    os.system("pip install --upgrade pip")
    os.system("pip install -r requirements.txt")
else:
    pip = input("键入你的pip管理工具的名称：")
    os.system(pip + "install --upgrade pip")
    os.system(pip + "install -r requirements.txt")

try:
    os.system("touch error.log && touch access.log")
    fp = open("config.ini", "w+")
    fp.write("[uwsgi]\n\nsocket = 127.0.0.1:5051\nchdir = /root/listen-now/\nwsgi-file = main.py\ncallable = app\nprocesses = 4\nthreads = 2\nstats = 127.0.0.1:9191\n")
    fp.close()
    content = """
    events {
        worker_connections  1024;
    }
    http {
        include       mime.types;    
        default_type  application/octet-stream;    
        sendfile        on;    
        keepalive_timeout  65;

        server {
            listen 80;     
            server_name 115.238.228.39;  
            access_log  /root/listen-now/project/access.log;   
            error_log  /root/listen-now/project/error.log;     

            location / {

                include        uwsgi_params;  

                uwsgi_pass     127.0.0.1:5051;  


                uwsgi_param UWSGI_PYHOME /root/listen-now/venv;   

                uwsgi_param UWSGI_CHDIR  /root/listen-now/;  

                uwsgi_param UWSGI_SCRIPT app:app;    
            }
        }
        server {
        listen 443;
        server_name www.zlclclc.cn; 
        ssl on;
        ssl_certificate 1_www.zlclclc.cn_bundle.crt;
        ssl_certificate_key 2_www.zlclclc.cn.key;
        ssl_session_timeout 5m;
        ssl_protocols TLSv1 TLSv1.1 TLSv1.2; 
        ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;
        ssl_prefer_server_ciphers on;
        location / {

            include        uwsgi_params;  

            uwsgi_pass     127.0.0.1:5051;  


            uwsgi_param UWSGI_PYHOME /root/listen-now/venv;   

            uwsgi_param UWSGI_CHDIR  /root/listen-now/;  

            uwsgi_param UWSGI_SCRIPT app:app;    
        }
    }

    }
    """
    fp = open("nginx.conf", "w+")
    fp.write(content)
    fp.close()
except:
    pass
else:
    print("[+]成功安装依赖环境!")





