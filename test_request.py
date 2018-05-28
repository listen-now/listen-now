#!usr/bin/env python3
# @File:test_request.py
# @Date:2018/05/28
# Author:Cat.1

import argparse

class test_request(object):


    def command(self):
        parser = argparse.ArgumentParser()        
        parser.add_argument("-t", dest  = "title", help    = "like: 白金迪斯科" )
        parser.add_argument("-p", dest  = "platform", help = "like: 网易(net)/QQ(qq)/虾米(xia)")
        parser.add_argument("-id", dest = "id", help       = "like 123456")
        args                            = parser.parse_args()
        title                           = args.title
        platform                        = args.platform
        music_id                        = args.id
        if music_id == None:
            print(title, platform)
        else:
            print(music_id, platform)


if __name__ == "__main__":
    test_user = test_request()
    test_user.command()