#!/usr/bin/env python3
# @File:music.py
# @Date:2018/05/28
# @Update:2018/06/11
# Author:Cat.1

import requests
import argparse
import json
import os
import re
import threading
import subprocess
import Logger


data = {
        "title":None,
        "platform":None,
        "page":1
        }


class pymusic(object):
    """pymusic类
    
    包括修正键入的字符方法(fix_enter)
    command方法用来接受用户的命令请求
    regex_func方法用来读入用户对歌曲的需求
    play_lyric方法用来开启异步线程来执行歌词播放
    player方法用来异步启用一个mpg123线程来播放音乐
    downloader方法还是一个不完善的办法
    Xia_Qq_Request_Play_Url用于请求虾米、QQ音乐的播放地址
    """
    def __init__(self):
        """
        初始化日志记录方法
        测试日志记录是否正常启用
        """
        music_logger = Logger.Logger('music_all.log', 'debug')
        music_logger.logger.debug('This is a test log.')

    def fix_enter(self, platform):
        """
        修正输入, 例如当你输入的是xia, net, qq时自动修正为
        Xiamimusic, Neteasymusic, QQmusic
        使得用户不需要按照一定的长度、规则去输入-p参数
        """
        platform_dict = {
                 "net":"Neteasymusic",
                 "qq":"QQmusic",
                 "xia":"Xiamimusic",
                }
        if len(platform) < 4:
            platform = platform_dict[platform]
        return platform

    def command(self):
        """
        主命令区, 这里接受用户的参数, 包括使用的-t、-p、-id、-uid等等都是在这里被解析的

        """
        global data

        parser                                                    = argparse.ArgumentParser()        
        parser.add_argument("-t", dest     = "title", help        = "like: 白金迪斯科" )
        parser.add_argument("-p", dest     = "platform", help     = "like: 网易(net)/QQ(qq)/虾米(xia)")
        parser.add_argument("-id", dest    = "id", help           = "like 123456")
        parser.add_argument("-page", dest  = "page", help         = "like 1")
        parser.add_argument("-uid", dest   = "userid", help       = "like 1")
        parser.add_argument("-sl", dest   = "songlist", help      = "like 236472")
        parser.add_argument("-r", dest   = "random_song", help    = "like random")

        args       = parser.parse_args()
        title      = args.title
        platform   = args.platform
        music_id   = args.id
        music_page = args.page
        userid     = args.userid
        songlist   = args.songlist
        random_song   = args.random_song

        if platform == None and userid == None and songlist == None:
            # 这里主要是判断一些参数是否为空, 猜测用户是想要执行什么指令, 根据猜测去构造
            # 需要的json包然后发送给远端服务器并接受远端服务器的响应
            # 再对响应进行解析即可播放
        
            print(os.system("pymusic -h"))
        else:
            platform = self.fix_enter(platform)
            if title != None:
                data["title"], data["page"], data["platform"]= title, 1, platform
                self.send_data("search", data, "post", music_page)
            elif music_id != None:
                data["id"], data["page"], data["platform"]= music_id, 1, platform
                self.send_data("id", data, "post", music_page)
            elif songlist != None:
                data = {"url":songlist}
                self.send_data("song_list_requests", data, "post", music_page)
            elif userid != None:
                data = {"uid":userid}
                self.send_data("user_song_list", data, "post", music_page)
            elif random_song != None:
                self.send_data("user_song_list", data, "get", music_page)

    def regex_func(self, content):
        # 判断用户是否需要单曲循环的方法
        
        if re.findall(r"\w{1,2}\s([\-c]+)", content):
            return 1

    def play_lyric(self, id):
        # 播放歌词的方法

        subprocess.call("read_lyric -id %s"%(id), shell=True)

    def player(self, play_url, loop=0):
        # 播放歌曲的方法
        try:
            if loop == 0:
                subprocess.call('mpg123 -q -v %s'%(play_url), shell=True)
            else:
                subprocess.call('mpg123 -q -v %s'%(play_url), shell=True)
        except:
            print("[-]出现技术故障, 请稍后再试, 或者换一首音乐")
    def downloader(self, play_url, loop=0):
        # 测试中的办法, 用来解决qq音乐的无法播放问题
        # 由于mpg123 bug引起的问题

        if loop == 0:
            music_file = requests.get(url=play_url)
            fp = open("mymusic", 'wb')
            fp.write(music_file.content)
            os.system('mpg123 -q -v mymusic')
        else:
            music_file = requests.get(url=play_url)
            fp = open("mymusic", 'wb')
            fp.write(music_file.content)
            os.system('mpg123 -q -v --loop -1 mymusic')

    def Xia_Qq_Request_Play_Url(self,platform, music_id='', media_mid='', songmid=''):
        # 用于请求虾米, qq音乐的播放地址的方法
        data = {
                "platform":platform,
                }
        if music_id != '':
            data["id"]  = music_id
        else:
            data["media_mid"] = media_mid
            data["songmid"]   = songmid
        resp = requests.post(url="http://zlclclc.cn/id", data=json.dumps(data))
        return resp

    def send_data(self, p, _send_data, func, music_page, w=""):
        # 发送数据包并解析数据包播放的方法.
        if music_page != None:
            _send_data["page"] = music_page

        if func == "post":
            try:
                resp = requests.post(url="http://zlclclc.cn/" + p, data=json.dumps(_send_data))
            except:
                print("[-]网络错误!")
            if p == "id":
                return resp
            if w == 1:
                return resp
            try:
                if resp.json()["code"] == "200":
                    for i in range(10):
                        try:
                            print("{0}".format(i), end="    ")
                            z = (50 - len(resp.json()[str(i)]["music_name"])) * " "
                            print("{0}".format(resp.json()[str(i)]["music_name"]), end=z)
                            print("{0}".format(resp.json()[str(i)]["artists"]))
                        except KeyError:
                            pass
                    print('\n')
                    try: 
                        keyboard = input(">>> Enter your select ")
                    except KeyboardInterrupt:
                        print("\n用户主动退出")
                        print("bye")
                    else:
                        try:
                            if len(keyboard) > 2:
                                newkeyboard = int(keyboard[:1])
                            else:
                                newkeyboard = int(keyboard)

                        except:
                            try:
                                music_page += 1
                                music_page -= 1
                            except TypeError:
                                music_page = 1

                            if keyboard == "s" and _send_data["page"] < 10:
                                _send_data["page"] = int(_send_data["page"]) + 1
                                music_page        += 1
                                return self.send_data(p, _send_data, func, music_page)
                            elif keyboard == "w" and _send_data["page"] > 0:
                                _send_data["page"] = int(_send_data["page"]) - 1
                                music_page        -= 1
                                return self.send_data(p, _send_data, func, music_page)
                        else:

                            if int(newkeyboard) >= 0 and int(newkeyboard) <= 10:
                                if self.regex_func(keyboard) == 1:
                                    # 单曲循环选项
                                    print('[~]如果没有音乐播放提示, 请检查您的网络情况')
                                    if _send_data["platform"] == "Neteasymusic":
                                        t1 = threading.Thread(target=self.player, args=(resp.json()[str(newkeyboard)]["play_url"], 1))
                                    elif _send_data["platform"] == "Xiamimusic":
                                        resp = self.Xia_Qq_Request_Play_Url(_send_data["platform"],
                                                                            resp.json()[str(newkeyboard)]["music_id"],
                                                                            )
                                    elif _send_data["platform"] == "QQmusic":

                                        resp = self.Xia_Qq_Request_Play_Url(_send_data["platform"],
                                                                            media_mid=resp.json()[str(newkeyboard)]["media_mid"],
                                                                            songmid=resp.json()[str(newkeyboard)]["songmid"],
                                                                            )
                                    t1 = threading.Thread(target=self.player, args=(resp.json()["0"]["play_url"], 0))
                                    t1.start()
                                    if t1.is_alive() and _send_data["platform"] == "Neteasymusic":
                                        t2 = threading.Thread(target=self.play_lyric, args=(resp.json()[str(newkeyboard)]["music_id"],))
                                        t2.start()
                                        t2.join()

                                    t1.join()
                                    # 暂时虾米音乐不启用歌词模块

                                else:
                                    # 不单曲循环的话
                                    if _send_data["platform"] == "Neteasymusic":
                                        t1 = threading.Thread(target=self.player, args=(resp.json()[str(newkeyboard)]["play_url"], 0))
                                    elif _send_data["platform"] == "Xiamimusic":
                                        resp = self.Xia_Qq_Request_Play_Url(_send_data["platform"],
                                                                            resp.json()[str(newkeyboard)]["music_id"],
                                                                            )

                                    elif _send_data["platform"] == "QQmusic":

                                        resp = self.Xia_Qq_Request_Play_Url(_send_data["platform"],
                                                                            media_mid=resp.json()[str(newkeyboard)]["media_mid"],
                                                                            songmid=resp.json()[str(newkeyboard)]["songmid"],
                                                                            )
                                    t1 = threading.Thread(target=self.player, args=(resp.json()["0"]["play_url"], 0))
                                    t1.start()
                                    
                                    if t1.is_alive() and _send_data["platform"] == "Neteasymusic":
                                        t2 = threading.Thread(target=self.play_lyric, args=(resp.json()[str(newkeyboard)]["music_id"],))
                                        t2.start()
                                        t2.join()
                                    t1.join()

                                print("[+]请选择新歌曲\n如果想要退出请按住Ctrl + c")
                                try:
                                    title = input(">>>请输入想要搜索的歌曲: ")
                                    if title == "exit()":
                                        print("bye")
                                        os.system("exit")
                                    platform = input(">>>请输入想要搜索的平台: ")
                                    if platform == "exit()":
                                        print("bye")
                                        os.system("exit")
                                    if title != None:
                                        music_page = 1
                                        platform = self.fix_enter(platform)
                                        _send_data["title"], _send_data["page"], _send_data["platform"]= title, 1, platform
                                        self.send_data(p, _send_data, func, music_page)

                                except KeyboardInterrupt:
                                    print("\n用户主动退出")
                                    print("bye")
                elif resp.json()["code"] == "201":
                    self.url_         = "http://music.163.com/song/media/outer/url?id=%s.mp3"
                    result = resp.json()
                    print(result["description"])
                    print("切换下一首歌请输入Ctrl + c\n\n")
                    print('[+]如果没有音乐播放提示, 请检查您的网络情况')
                    for i in range(int(result["song_num"])):
                        music_name                          = result["Songlist_detail"][i]["name"]
                        music_id                            = result["Songlist_detail"][i]["id"]
                        artists                             = result["Songlist_detail"][i]["ar"][0]["name"]
                        print("{0}".format(music_name), end ="    ")
                        print("{0}".format(artists))
                        t1                                  = threading.Thread(target=self.player, args=(self.url_ %(music_id),))
                        t1.start()
                        if t1.is_alive():
                            t2                                  = threading.Thread(target=self.play_lyric, args=(music_id,))
                            t2.start()
                        t1.join()
                        # t2.join()

                elif resp.json()["code"] == "202":
                    result = resp.json()
                    for i in range(int(result["Sum_Song_List"])):
                        print("{0}".format(i), end = "   ")
                        print("{0}".format(result[str(i)]["Playlist_name"]))
                    try:
                        keyboard = input(">>> Enter your select ")
                    except KeyboardInterrupt:
                        print("\n用户主动退出")
                        print("bye")
                    else:
                        pass
                        # if keyboard == "s" and _send_data["page"] < 10:
                        #     _send_data["page"] = int(_send_data["page"]) + 1
                        #     music_page        += 1
                        #     return self.send_data(p, _send_data, func, music_page)
                        # elif keyboard == "w" and _send_data["page"] > 0:
                        #     _send_data["page"] = int(_send_data["page"]) - 1
                        #     music_page        -= 1
                        #     return self.send_data(p, _send_data, func, music_page)
                    
                    os.system('pymusic -sl %s -p net'%(result[str(keyboard)]["Playlist_id"]))
                else:
                    print(resp.json())
                    print("服务器繁忙!")
            except KeyError:
                print("\n[-]没有更多关于这首歌的内容\n")

        else:
            resp = requests.get(url="http://zlclclc.cn/" + p)
            print(resp.json())

if __name__ == "__main__":
    test_user = pymusic()
    test_user.command()

