#!/usr/bin/env python3
# @File:set_init.py
# @Date:FileDate
# Author:Cat.1

import os
import sys


path1 = "sudo ln -s " + os.path.abspath('.') + "/music.py " + "/usr/local/bin/pymusic" 
path2 = "sudo ln -s " + os.path.abspath('.') + "/read_lyric.py " + "/usr/local/bin/read_lyric" 

try:
    os.system(path1)
    os.system(path2)

except:
    print("[-]请手动初始化终端命令功能")
    print("参考指令 -> " + path)
else:
    print("[+]终端命令初始化成功!")

try:
    platform = sys.platform
except:
    print("识别操作系统时发现未知错误")
else:
    if platform == "darwin":
        os.system("brew install mpg123")
    elif platform == "linux":
        os.system("sudo apt-get install mpg123")
        os.system("sudo yum install mpg123")
    else:
        print("暂时不支持Win平台")

try:
    os.system("pip3 install -r requirement.txt")
except:
    print("安装Python依赖环境出现错误")
else:
    print("[]")