#!/usr/bin/env python3
# @File:music.py
# @Date:2018/05/28
# Author:Cat.1

import requests
import argparse
import json
import os

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
        args       = parser.parse_args()
        title      = args.title
        platform   = args.platform
        music_id   = args.id
        music_page = args.page
        userid     = args.userid

        if platform == None and userid == None:
            print(os.system("pymusic -h"))
        else:
            platform = self.fix_enter(platform)
            if music_id == None:
                data["title"], data["page"], data["platform"]= title, 1, platform
                self.send_data("search", data, "post", music_page)
            else:
                data["id"], data["page"], data["platform"]= music_id, 1, platform
                self.send_data("id", data, "post", music_page)


    def send_data(self, p, _send_data, func, music_page):

        if music_page != None:
            _send_data["page"] = music_page

        if func == "post":
            resp = requests.post(url="http://zlclclc.cn/" + p, data=json.dumps(_send_data))
            try:
                if resp.json()["code"] == "200":
                    for i in range(11):
                        try:
                            print(str(i), end="    ")
                            print(resp.json()[str(i)]["music_name"], end="    ")
                            print(resp.json()[str(i)]["artists"])
                        except KeyError:
                            pass
                    try: 
                        keyboard = input(">>>Enter your select ")
                    except KeyboardInterrupt:
                        print("\n用户主动退出")
                        print("bye")
                    else:
                        try:
                            int(keyboard)
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
                            if int(keyboard) >= 0 or int(keyboard) <= 10:
                                os.system('mpg123 -q -v "%s"'%(resp.json()[keyboard]["play_url"]))

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
                else:
                    print(resp.json())
                    print("服务器繁忙!")
            except KeyError:
                print("\n[~]没有更多关于这首歌的内容\n")
        else:
            requests.get(url="http://zlclclc.cn/" + p)

if __name__ == "__main__":
    test_user = test_request()
    test_user.command()
