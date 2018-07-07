#!/usr/bin/env python3
# @File:read_lyric.py
# @Date:2018/06/03
# Author:Cat.1
import time , re
import subprocess
import argparse
import requests, json
from colorama import  init, Fore, Back, Style  


class Colored(object):  
  
    #  前景色:红色  背景色:默认  
    def red(self, s):  
        return Fore.RED + s + Fore.RESET  
  
    #  前景色:绿色  背景色:默认  
    def green(self, s):  
        return Fore.GREEN + s + Fore.RESET  
  
    #  前景色:黄色  背景色:默认  
    def yellow(self, s):  
        return Fore.YELLOW + s + Fore.RESET  
  
    #  前景色:蓝色  背景色:默认  
    def blue(self, s):  
        return Fore.BLUE + s + Fore.RESET  
  
    #  前景色:洋红色  背景色:默认  
    def magenta(self, s):  
        return Fore.MAGENTA + s + Fore.RESET  
  
    #  前景色:青色  背景色:默认  
    def cyan(self, s):  
        return Fore.CYAN + s + Fore.RESET  
  
    #  前景色:白色  背景色:默认  
    def white(self, s):  
        return Fore.WHITE + s + Fore.RESET  
  
    #  前景色:黑色  背景色:默认  
    def black(self, s):  
        return Fore.BLACK  
  
    #  前景色:白色  背景色:绿色  
    def white_green(self, s):  
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET  


class Play_Lyric(object):
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
            lyric    = _lyric[i] + ", "+ _lyric[i+1]
        except IndexError:
            lyric    = _lyric[i]
        TimeList = re.findall(r"\d{1,3}\:\d{1,3}\.\d{1,3}", lyric)
        lyric    = re.sub(r"\d{1,3}\:\d{1,3}\.\d{1,3}", '', lyric)
        lyric    = lyric.replace('[]','')

        if len(TimeList) > 1:
            TimeEnd   = TimeList[1].split(':')
            TimeStart = TimeList[0].split(':')
            Time_diff = int(TimeEnd[0])-int(TimeStart[0])
            if Time_diff > 0:
                Time_diff = Time_diff * 60

        if isinstance(TimeEnd, list) and TimeList != []:
            TimeSleep = float(Time_diff + (float(TimeEnd[1]) - float(TimeStart[1])))
        # print("{0:_^60}".format(lyric))
        lyric = "{0:_^60}".format(lyric)
        print(lyric)
        # color = Colored()
        # for i in range(len(lyric)):
            # print(lyric, end='')
            # print(color.red(lyric[i]), end='')
            # time.sleep(TimeSleep%len(lyric))
        # print(TimeSleep/len(lyric))
        # time.sleep(10)
        time.sleep(TimeSleep)
        subprocess.call("clear")

        if TimeList == []:
            print("{0:_^60}".format(lyric))
            time.sleep(2)
            subprocess.call("clear")






