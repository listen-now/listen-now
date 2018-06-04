#!/usr/bin/env python3
# @File:music.py
# @Date:2018/05/28
# Author:Cat.1

import requests
import argparse
import json
import os
import re
import threading
import subprocess

data = {
        "title":None,
        "platform":None,
        "page":1
        }


class test_request(object):

    def fix_enter(self, platform):
        platform_dict = {
                 "net":"Neteasymusic",
                 "qq":"QQmusic",
                 "xia":"Xiamimusic",
                }
        if len(platform) < 4:
            platform = platform_dict[platform]
        return platform

    def command(self):
        global data

        parser                                                    = argparse.ArgumentParser()        
        parser.add_argument("-t", dest     = "title", help        = "like: 白金迪斯科" )
        parser.add_argument("-p", dest     = "platform", help     = "like: 网易(net)/QQ(qq)/虾米(xia)")
        parser.add_argument("-id", dest    = "id", help           = "like 123456")
        parser.add_argument("-page", dest  = "page", help         = "like 1")
        parser.add_argument("-uid", dest   = "userid", help       = "like 1")
        parser.add_argument("-sl", dest   = "songlist", help      = "like 236472")
        parser.add_argument("-r", dest   = "random_song", help       = "like random")

        args       = parser.parse_args()
        title      = args.title
        platform   = args.platform
        music_id   = args.id
        music_page = args.page
        userid     = args.userid
        songlist   = args.songlist
        random_song   = args.random_song

        if platform == None and userid == None and songlist == None:
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
        if re.findall(r"\w{1,2}\s([\-c]+)", content):
            return 1

    def play_lyric(self, id):
        subprocess.call("read_lyric -id %s"%(id), shell=True)
    def player(self, play_url):
        # subprocess.call('mpg123 -q -v "%s"'%(play_url))
        os.system('mpg123 -q -v "%s"'%(play_url))

        subprocess.call('mpg123 -q -v "%s"'%(play_url))
    def send_data(self, p, _send_data, func, music_page, w=""):

        if music_page != None:
            _send_data["page"] = music_page

        if func == "post":
            try:
                resp = requests.post(url="http://zlclclc.cn/" + p, data=json.dumps(_send_data))
            except:
                print("[-]网络错误!")
            if w == 1:
                return resp
            try:
                if resp.json()["code"] == "200":
                    for i in range(10):
                        try:
                            print(str(i), end="      ")
                            print(resp.json()[str(i)]["music_name"], end="      ")
                            print(resp.json()[str(i)]["artists"])
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
                            if keyboard == "s" and _send_data["page"] < 10:
                                _send_data["page"] = int(_send_data["page"]) + 1
                                music_page        += 1
                                return self.send_data(p, _send_data, func, music_page)
                            elif keyboard == "w" and _send_data["page"] > 0:
                                _send_data["page"] = int(_send_data["page"]) - 1
                                music_page        -= 1
                                return self.send_data(p, _send_data, func, music_page)
                        else:
                            if int(newkeyboard) >= 0 or int(newkeyboard) <= 10:
                                # self.regex_func 反馈1表示用户需要单曲循环
                                if self.regex_func(keyboard) == 1:
                                    os.system('mpg123 -q -v --loop -1 "%s"'%(resp.json()[str(newkeyboard)]["play_url"]))
                                else:
                                    t1 = threading.Thread(target=self.player, args=(resp.json()[str(newkeyboard)]["play_url"],))
                                    t2 = threading.Thread(target=self.play_lyric, args=(resp.json()[str(newkeyboard)]["music_id"],))
                                    t1.start()
                                    t2.start()
                                    t1.join()
                                    t2.join()
                                    # os.system('mpg123 -q -v "%s"'%(resp.json()[str(newkeyboard)]["play_url"]))

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
                    for i in range(int(result["song_num"])):
                        music_name = result["Songlist_detail"][i]["name"]
                        music_id   = result["Songlist_detail"][i]["id"]
                        artists    = result["Songlist_detail"][i]["ar"][0]["name"]
                        print(music_name, end="      ")
                        print(artists)
                        os.system('mpg123 -q -v "%s"'%(self.url_ %(music_id)))
                elif resp.json()["code"] == "202":
                    result = resp.json()
                    for i in range(int(result["Sum_Song_List"])):
                        print(i, end = "     ")
                        print(result[str(i)]["Playlist_name"])
                    try: 
                        keyboard = input(">>> Enter your select ")
                    except KeyboardInterrupt:
                        print("\n用户主动退出")
                        print("bye")
                        # else:
                        #     if keyboard == "s" and _send_data["page"] < 10:
                        #         _send_data["page"] = int(_send_data["page"]) + 1
                        #         music_page        += 1
                        #         return self.send_data(p, _send_data, func, music_page)
                        #     elif keyboard == "w" and _send_data["page"] > 0:
                        #         _send_data["page"] = int(_send_data["page"]) - 1
                        #         music_page        -= 1
                        #         return self.send_data(p, _send_data, func, music_page)
                    os.system('pymusic -sl %s -p net'%(result[str(keyboard)]["Playlist_id"]))
                else:
                    print(resp.json())
                    print("服务器繁忙!")
            except ImportError:
                print("\n[~]没有更多关于这首歌的内容\n")
        else:
            resp = requests.get(url="http://zlclclc.cn/" + p)
            print(resp.json())

if __name__ == "__main__":
    test_user = test_request()
    test_user.command()
    # test_user.regex_func('5 -c')