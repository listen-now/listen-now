#!usr/bin/env python3
# @File:Hot_Song_List.py
# @Date:2018/05/22
# Author:Cat.1

import requests
import re, random
import redis, time
import sys
sys.path.append("..")
import encrypt.AES
import config.config


Page_Start_Url = "/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset="
Page_Start     = 35
Raw_Page_Sum   = 0

class Hot_Song_List(object):
    requ_date        = {}

    """
    这个类用于维护用户热门歌单信息，在redis-1号数据库中，
    储存每一个热门歌单的歌单地址，歌单封面，歌单名称
    因为redis的key-value关系，所以储存的内容类似以下格式：
    http://p1.music.126.net/9Ctz52eQqDwaFd7LBMyyiw==/109951163313760940.jpg?
    user_song_list\xe7\x88\xb5\xe5\xa3\xab\xe6\x83\x85\
    user_song_list/playlist?id=2101648512
    以"user_song_list"作为分隔符，分别信息为歌单封面，歌单名称，歌单地址
    """


    def __init__(self):
        self.session = requests.session()
        self.headers = {
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13;rv:57.0) Gecko/20100101 Firefox/57.0',
                        'Referer':"http://music.163.com"
                        }
        self.post_headers  = {
                            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13;rv:57.0) Gecko/20100101 Firefox/57.0',
                            'Referer':"http://music.163.com", 
                            'Content-Type':"application/x-www-form-urlencoded"
                             }
        self.User_List_All = ["用户热门歌单",\
                             "/discover/playlist"]
        if int(config.config.getConfig("open_database", "redis")) == 1:
            host               = config.config.getConfig("database", "dbhost")
            port               = config.config.getConfig("database", "dbport")
            self.r             = redis.Redis(host=host, port=int(port), decode_responses=True, db = 1)  
            # 连接到redis-1号数据库, 用于储存网易云音乐的用户热门歌单信息
            self.NEMurl        = "http://music.163.com"

    def pre_request(self, url, proxies=''):
        """
        这个类用于维护redis-1更新
        更新的内容为热门歌单数据
        储存格式范例已经在类的说明中说明
        """
        global Page_Start_Url, Page_Start, Raw_Page_Sum
        if proxies == '':
            resp           = self.session.get(url=self.NEMurl + url, headers=self.headers)  
        else:
            resp           = self.session.get(url=self.NEMurl + url, headers=self.headers, proxies=proxies)
        try:
            regex          = re.compile(r"\<img class=\"[\w0-9\-]+\" src=\"(.+)\"\/>\n<a title=\"([\｜\✞\♪\(\)\？\?\♡\【\¼\】\/\[\]\丨\s\「\」\|\『\』\——\•\★\"\u4e00-\u9fa5\w\d\s\，\.]+)\" href=\"(.+)\" class=")
            result         = regex.findall(resp.text)
            regex          = re.compile(r"<a href=\"(.+)\" class=\"zpgi\">\d{1,3}</a>")
            Page_Url       = regex.findall(resp.text)

            Limit_Max_Page = int(re.findall(r'offset=(\d{2,5})', Page_Url[-1])[0])
        except:
            host       = config.config.getConfig("database", "dbhost")
            port       = config.config.getConfig("database", "dbport")
            self.r     = redis.Redis(host=str(host),port=int(port),db=4)
            random_int = random.sample(range(0, self.r.dbsize()), 1)
            proxies    = self.r.get(str(random_int[0]))
            self.pre_request(url, eval(proxies))

        Raw_Page_Sum   = 0
        for i in range(Raw_Page_Sum, Raw_Page_Sum + len(result)):
            self.r.set(str(i), result[i - Raw_Page_Sum][0] + "user_song_list" + result[i - Raw_Page_Sum][1] + "user_song_list" + result[i - Raw_Page_Sum][2])
        print("Update")
        Raw_Page_Sum   += len(result)
        print(Raw_Page_Sum)
        regex          = re.compile(r"<a href=\"(.+)\" class=\"zpgi\">\d{1,3}</a>")
        Page_Url       = regex.findall(resp.text)

        Limit_Max_Page = int(re.findall(r'offset=(\d{2,5})', Page_Url[-1])[0])
        if Page_Start <= Limit_Max_Page:
            Page_Start += 35
            url = Page_Start_Url + str(Page_Start)
            time.sleep(5)
            test.pre_request(url)
        else:
            return 1

    def Random_Return_func(self):
        """
        这个方法用于向前端随机返回redis-1数据库中的六条歌单记录
        """
        global re_date
        self.requ_date = {}
        Random_Max = self.r.dbsize()
        for i in range(0, 6):
            music_data = {}
            
            User_Song_List = self.r.get(str(random.sample(range(0, Random_Max), 1)[0]))
            music_data.update({
                                "image_url":User_Song_List.split("user_song_list")[0],\
                                "title": User_Song_List.split("user_song_list")[1], \
                                "song_list_url": self.NEMurl + User_Song_List.split("user_song_list")[2]
                                })
            self.requ_date.update({str(i) : music_data})
        return self.requ_date
    
    @staticmethod
    def Download_SongList(url):
        post_headers  = {
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13;rv:57.0) Gecko/20100101 Firefox/57.0',
                        'Referer':"http://music.163.com", 
                        'Content-Type':"application/x-www-form-urlencoded"
                        }
        requ_date = {}
        """
        这是用来下载用户的歌单的方法
        并向前端返回歌曲的id,歌手, 歌名的信息
        通过独一无二的歌曲id请求Scrawl_Neteasymusic.py中的music_id_requests方法返回
        单首歌曲详细信息
        """
        date = "{\'id\': %s, \'total\': \'true\',\'csrf_token\
        \':\"\", \'limit\': 1000, \'n\': 1000, \'offset\': 0}"
        Song_List_Id = re.findall(r"id=(\d{1,15})", url)
        if Song_List_Id == []:
            Song_List_Id = re.findall(r"(\d{1,15})", url)
        date = encrypt.AES.encrypted_request(date %(Song_List_Id[0]))
        try:
            connection = requests.session().post(url="http://music.163.com/weapi/v3/playlist/detail",
                                           data=date,
                                           headers=post_headers,
                                           )
        except EOFError:
            return 0
        else:
            try:
                music_data = {}
                connection = connection.json()
                num = len(connection["playlist"]['tracks'])
                music_data = {"creator":connection["playlist"]['creator'], "Songlist_detail":connection["playlist"]['tracks'], "description":connection["playlist"]['description'], "song_num":num}
            except:
                music_data = {"status":"没有该歌单!"}
            requ_date.update(music_data)
            return requ_date


if __name__ == "__main__":
    
    test = Hot_Song_List()
    while 1:
        test.pre_request(test.User_List_All[1])
        time.sleep(3600 * 24)
        test.r.flushdb()
    # print(Hot_Song_List.Download_SongList("2196054076"))
