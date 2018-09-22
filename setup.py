#!/usr/bin/env python3
# @File:setup.py
# @Date:2018/07/15 Cat.1
# @Update:2018/09/01 Cat.1
# @Update:2018/09/22 Cat.1
# Author:Cat.1


import os
import sys
import platform
import subprocess



path1    = "sudo ln -s " + os.path.abspath('.') + "/project/Pymusic/music.py " + "/usr/local/bin/pymusic" 
path2    = "sudo ln -s " + os.path.abspath('.') + "/project/Pymusic/read_lyric.py " + "/usr/local/bin/read_lyric" 
command1 = "mkdir /var/log/Listen-now/"
chmodCommand = "sudo chmod 777 /var/log/Listen-now"
command2 = "touch /var/log/Listen-now/Listen-now.log"
            


try:
    try:
        print("Hello " + os.getlogin()+" 我们正在为您执行listen-now的后端自动化部署")
    except FileNotFoundError:
        # 无法判断用户身份，无法得到用户的用户名，使用默认用户名来输出
        print("Hello Listen-now用户, 我们正在为您执行listen-now的后端自动化部署")
    # 执行相关操作，包括建立pymusic的软链接和在/var/log/下建立日志文件用于后端错误分析
    subprocess.check_output(path1, shell=True).decode("UTF-8")
    subprocess.check_output(path2, shell=True).decode("UTF-8")
    subprocess.check_output(command1, shell=True).decode("UTF-8"))
    subprocess.check_output(chmodCommand, shell=True).decode("UTF-8"))
    subprocess.check_output(command2, shell=True).decode("UTF-8"))

except:
    print("[-]请手动初始化以下内容\n")
    print("参考指令列表：\n")
    print(path1 + "\n" +path2 + "\n" + command1 + "\n" + command2 + "\n" + chmodCommand)

else:
    print("[+]终端命令初始化成功!")


try:
    platform = sys.platform
except:
    print("[-]识别操作系统时发现未知错误")
    raise BaseException
else:
    try:
        if platform == "darwin":
            print(subprocess.check_output("brew install mpg123", shell=True).decode("UTF-8"))
            print(subprocess.check_output("brew install ffmpeg", shell=True).decode("UTF-8"))
        elif platform == "linux":
            platform = {"1":"基于Redhat的发行版及centos", "2":"debian及基于debian的发行版"}
            platform = platform[input("请选择你的linux版本\n1.)基于Redhat的发行版及centos\n2.)debian及基于debian的发行版\n->")]
            if platform == "基于Redhat的发行版及centos":
                print(subprocess.check_output("sudo yum -y install mpg123", shell=True).decode("UTF-8"))
                print(subprocess.check_output("sudo yum -y install ffmpeg", shell=True).decode("UTF-8"))
            elif platform == "debian及基于debian的发行版":
                print(subprocess.check_output("sudo apt-get -y install mpg123", shell=True).decode("UTF-8"))
                print(subprocess.check_output("sudo apt-get -y install ffmpeg", shell=True).decode("UTF-8"))
        else:
            print("暂时不支持Win平台")
            raise BaseException
    except:
        print("[-]安装环境出现错误，请手动执行")
        print("请手动安装 ffmpeg, mpg123\n\n")
        

# 关于判断用户的Python版本中pip的构建问题
pip = {"1":"pip", "2":"pip3", "3":"other"}
pip = pip[input("请选择你的pip管理工具使用的哪一个名称\n1.)pip\n2.)pip3\n3.)other\n->")]
try:
    if pip == "pip3":
        print(subprocess.check_output("sudo pip3 install --upgrade pip", shell=True).decode("UTF-8"))
        print(subprocess.check_output("sudo pip3 install -r requirements.txt", shell=True).decode("UTF-8"))
    elif pip == "pip":
        print(subprocess.check_output("sudo pip install --upgrade pip", shell=True).decode("UTF-8"))
        print(subprocess.check_output("sudo pip install --upgrade pip", shell=True).decode("UTF-8"))
    else:
        pip = input("键入你的pip管理工具的名称：")
        print(subprocess.check_output("sudo " + pip + " install --upgrade pip", shell=True).decode("UTF-8"))
        print(subprocess.check_output("sudo " + pip + " install --upgrade pip", shell=True).decode("UTF-8"))
except:
    print("[-]pip依赖包安装失败")
    print("请手动安装requirements.txt")

try:
    print(subprocess.check_output("touch error.log && touch access.log", shell=True).decode("UTF-8"))
    # nginx的日志文件直接放在了当前目录下，并做映射到Log目录中的NginxAccess.log & NginxError.log
    subprocess.check_output("ln -s access.log ./project/Log/NginxAccess.log && ln -s error.log ./project/Log/NginxError.log")
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
    print("[-]写入nginx或uwsgi配置文件失败")
    raise BaseException
else:
    print("[+]成功安装依赖环境!")







