#!usr/bin/env python3
# @File:test_request.py
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
        global data

        parser = argparse.ArgumentParser()        
        parser.add_argument("-t", dest  = "title", help    = "like: 白金迪斯科" )
        parser.add_argument("-p", dest  = "platform", help = "like: 网易(net)/QQ(qq)/虾米(xia)")
        parser.add_argument("-id", dest = "id", help       = "like 123456")
        args                            = parser.parse_args()
        title                           = args.title
        platform                        = args.platform
        music_id                        = args.id

        if music_id == None:
            data["title"], data["page"], data["platform"]= title, 1, platform
            self.send_data("search", data, "post")
        else:
            data["id"], data["page"], data["platform"]= music_id, 1, platform
            self.send_data("id", data, "post")


    def send_data(self, p, _send_data, func):
        if func == "post":
            resp = requests.post(url="http://127.0.0.1:8888/" + p, data=json.dumps(_send_data))
            os.system('mpg123 "%s"'%(resp.json()["0"]["play_url"]))

        else:
            requests.get(url="http://127.0.0.1:8888/" + p)


if __name__ == "__main__":
    test_user = test_request()
    test_user.command()