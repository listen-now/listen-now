#!/usr/bin/env python3
# @File:set_init.py
# @Date:FileDate
# Author:Cat.1

import os
import sys
import platform

path1 = "sudo ln -s " + os.path.abspath('.') + "/music.py " + "/usr/local/bin/pymusic" 
path2 = "sudo ln -s " + os.path.abspath('.') + "/read_lyric.py " + "/usr/local/bin/read_lyric" 

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
        platform = {"1":"centos", "2":"ubuntu"}
        platform = platform[print("请选择你的linux版本\n1.)centos\n2.)ubuntu")]
        if platform == "centos":
            os.system("sudo yum install mpg123")
            os.system("sudo yum install ffmpeg")
        elif platform == "ubuntu": 
            os.system("sudo apt-get install mpg123")
            os.system("sudo apt-get install ffmpeg")
    else:
        print("暂时不支持Win平台")

# 关于判断用户的Python版本中pip的构建问题
pip = {"1":"pip", "2":"pip3", "3":"other"}
pip = pip[print("请选择你的pip管理工具使用的哪一个名称\n1.)pip\n2.)pip3\n3.)other")]
    if pip == "pip3":
        os.system("pip3 install --upgrade pip")
        os.system("pip3 install -r requirements.txt")
    elif pip == "pip":
        os.system("pip install --upgrade pip")
        os.system("pip install -r requirements.txt")
    else:
        pip = print("键入你的pip管理工具的名称：")
        os.system(pip + "install --upgrade pip")
        os.system(pip + "install -r requirements.txt")
    
    print("[+]成功安装依赖环境!")





