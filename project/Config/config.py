#!usr/bin/env python3
# @File:Config.py
# @Date:2018/05/19
# Author:Cat.1
# encoding:utf-8

try:
    import configparser
except:
    from six.moves import configparser 
import os

#获取config配置文件
def getConfig(section, key):
    config = configparser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/setting.conf'
    config.read(path)
    return config.get(section, key)
