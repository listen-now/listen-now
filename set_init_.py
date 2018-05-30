#!/usr/bin/env python3
# @File:set_init.py
# @Date:FileDate
# Author:Cat.1
import os

path = "sudo ln -s " + os.path.abspath('.') + "/music.py " + "/usr/local/bin/pymusic" 
try:
    os.system(path)
    raise ArithmeticError
except:
    print("[-]请手动初始化终端命令功能")
    print("参考指令 -> " + path)
else:
    print("[+]终端命令初始化成功!")


