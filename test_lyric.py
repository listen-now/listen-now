#!/usr/bin/env python3
# @File:test_lyric.py
# @Date:2018/06/05
# Author:Cat.1

import re, time


_lyric = _lyric.split("\n")

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
    TimeSleep = int(Time_diff + (float(TimeEnd[1]) - float(TimeStart[1])))
    print(lyric)
    print(TimeSleep)
    time.sleep(TimeSleep)
