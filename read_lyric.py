#!/usr/bin/env python3
# @File:read_lyric.py
# @Date:2018/06/03
# Author:Cat.1
import time , re
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

resp      = requests.post(url="http://zlclclc.cn/id", data=json.dumps(_send_data))
_lyric    = resp.json()["0"]["lyric"].split("\n")

Time_diff,TimeEnd, TimeStart, TimeSleep= 0, 0, 0, 0

for i in range(len(_lyric)):
    try:
        lyric    = _lyric[i] + _lyric[i+1]
    except IndexError:
        lyric    = _lyric[i]
    TimeList = re.findall(r"\d{2}\:\d{2}\.\d{3}", lyric)
    lyric    = re.sub(r"\d{2}\:\d{2}\.\d{3}", '', lyric)
    lyric    = lyric.replace('[]','')
    if len(TimeList) > 1:
        TimeEnd   = TimeList[1].split(':')
        TimeStart = TimeList[0].split(':')
        Time_diff = int(TimeEnd[0])-int(TimeStart[0])
        if Time_diff > 0:
            Time_diff = Time_diff * 60
    if TimeEnd[0] != None:
        TimeSleep = int(Time_diff + (float(TimeEnd[1]) - float(TimeStart[1])))
    print("{0:_^60}".format(lyric))
    time.sleep(TimeSleep)
    subprocess.call("clear")
