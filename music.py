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


    def command(self):
        global data, n
        platform_dict = {
                         "net":"Neteasymusic",
                         "qq":"QQmusic",
                         "xia":"Xiamimusic",
                        }

        parser                                      = argparse.ArgumentParser()        
        parser.add_argument("-t", "--title", dest   = "title", help     = "like: 白金迪斯科" )
        parser.add_argument("-p", "--platform",dest = "platform", help  = "like: 网易(net)/QQ(qq)/虾米(xia)")
        parser.add_argument("-id", "--musicid",dest = "id", help        = "like 123456")
        parser.add_argument("-n", "--number", dest  = "num", help       = "like 1")
        parser.add_argument("-page", dest  = "page", help       = "like 1")

        args       = parser.parse_args()
        n          = args.num
        title      = args.title
        platform   = args.platform
        music_id   = args.id
        music_page = args.page
        if platform == None:
            print(os.system("pymusic -h"))
        else:
            if len(platform) < 4:
                platform = platform_dict[platform]
            if music_id == None:
                data["title"], data["page"], data["platform"]= title, 1, platform
                self.send_data("search", data, "post", music_page)
            else:
                data["id"], data["page"], data["platform"]= music_id, 1, platform
                self.send_data("id", data, "post", music_page)


    def send_data(self, p, _send_data, func, music_page):
        global n
        if music_page != None:
            _send_data["page"] = music_page

        if func == "post":
            resp = requests.post(url="http://zlclclc.cn/" + p, data=json.dumps(_send_data))

            try:
                # print(resp.json())
                if resp.json()["code"] == "200":
                    for i in range(11):
                        try:
                            print(str(i), end="    ")
                            print(resp.json()[str(i)]["music_name"], end="    ")
                            print(resp.json()[str(i)]["artists"])
                        except KeyError:
                            pass
                    keyboard = input(">>>Enter your select ")
                    try:
                        int(keyboard)
                    except:
                        if keyboard == "s" and _send_data["page"] < 10:
                            _send_data["page"] = int(_send_data["page"]) + 1
                            return self.send_data(p, _send_data, func, music_page)
                        elif keyboard == "w" and _send_data["page"] > 0:
                            _send_data["page"] = int(_send_data["page"]) - 1
                            return self.send_data(p, _send_data, func, music_page)
                    else:

                        if int(keyboard) >= 0 or int(keyboard) <= 10:
                        # try:
                            os.system('mpg123 "%s"'%(resp.json()[keyboard]["play_url"]))
                        # except KeyboardInterrupt:
                            print("[+]请选择新歌曲\n如果想要退出请按住Ctrl + c")
                            try:
                                title = input(">>>Enter your search music: ")
                                platform = input(">>>Enter your search platform: ")
                                if title != None:
                                    music_page = 1
                                    _send_data["title"], _send_data["page"], _send_data["platform"]= title, 1, platform
                                    send_data(p, _send_data, func, music_page)
                            except KeyboardInterrupt:
                                print("用户主动退出")
                                print("bye")

            except KeyError:
                print("\n[~]没有更多关于这首歌的内容\n")

        else:
            requests.get(url="http://zlclclc.cn/" + p)

if __name__ == "__main__":
    test_user = test_request()
    test_user.command()
