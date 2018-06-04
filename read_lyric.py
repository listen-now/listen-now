#!/usr/bin/env python3
# @File:read_lyric.py
# @Date:2018/06/03
# Author:Cat.1
import time 
import subprocess
import argparse
import requests, json

parser = argparse.ArgumentParser()        
parser.add_argument("-id", dest = "id", help = "like 123456")
args = parser.parse_args()

music_id   = args.id

music_page = 1

_send_data = {
             "id":music_id,
             "platform":"Neteasymusic",
             "page":music_page
             }

resp = requests.post(url="http://zlclclc.cn/id", data=json.dumps(_send_data))


for i in resp.json()["0"]["lyric"].split("\n"):
    print(">>>", i , "<<<")
    time.sleep(2)
    subprocess.call("clear")
