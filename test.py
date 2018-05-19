#!usr/bin/env python3
# @File:flush_NEM.py
# @Date:2018/05/19
# Author:Cat.1

import redis, time
import requests, re
from requests import RequestException
import AES
import config


class NEM(object):
    """
    This is a base sarwl , include class, and use requests.session 
    and requests.get/post
    """
    def __init__(self):
        self.top_list_all = {
                        0: ['云音乐新歌榜', '/discover/toplist?id=3779629'],
                        1: ['云音乐热歌榜', '/discover/toplist?id=3778678'],
                        2: ['网易原创歌曲榜', '/discover/toplist?id=2884035'],
                        3: ['云音乐飙升榜', '/discover/toplist?id=19723756'],
                        4: ['云音乐电音榜', '/discover/toplist?id=10520166'],
                        5: ['UK排行榜周榜', '/discover/toplist?id=180106'],
                        6: ['美国Billboard周榜', '/discover/toplist?id=60198'],
                        7: ['KTV嗨榜', '/discover/toplist?id=21845217'],
                        8: ['iTunes榜', '/discover/toplist?id=11641012'],
                        9: ['Hit FM Top榜', '/discover/toplist?id=120001'],
                        10: ['日本Oricon周榜', '/discover/toplist?id=60131'],
                        11: ['韩国Melon排行榜周榜', '/discover/toplist?id=3733003'],
                        12: ['韩国Mnet排行榜周榜', '/discover/toplist?id=60255'],
                        13: ['韩国Melon原声周榜', '/discover/toplist?id=46772709'],
                        14: ['中国TOP排行榜(港台榜)', '/discover/toplist?id=112504'],
                        15: ['中国TOP排行榜(内地榜)', '/discover/toplist?id=64016'],
                        16: ['香港电台中文歌曲龙虎榜', '/discover/toplist?id=10169002'],
                        17: ['华语金曲榜', '/discover/toplist?id=4395559'],
                        18: ['中国嘻哈榜', '/discover/toplist?id=1899724'],
                        19: ['法国 NRJ EuroHot 30周榜', '/discover/toplist?id=27135204'],
                        20: ['台湾Hito排行榜', '/discover/toplist?id=112463'],
                        21: ['Beatport全球电子舞曲榜', '/discover/toplist?id=3812895']
                        }
        self.User_List_All = ["用户热门歌单", "/discover/playlist"]
        host = config.getConfig("database", "dbhost")
        port = config.getConfig("database", "dbport")
        self.r       = redis.Redis(host=host, port=port, decode_responses=True)  
        self.session = requests.session()
        self.headers = {
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
                        'Referer':'http://music.163.com/',
                        'Content-Type':'application/x-www-form-urlencoded'
                        }
        self.play_url     = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
        self.br           = "128000"
        self.play_default = "{\"ids\":\"[%s]\",\"br\":%s\
        ,\"csrf_token\":\"\"}"


    def top_songlist(self, url):
        
        connection = requests.get(url = url,
                                  headers=self.headers,
                                  )
        connection.encoding = 'UTF-8'
        songids = re.findall(r'/song\?id=(\d+)', connection.text)
        songids = set(songids)
        if songids == []:
            return 0
        return list(songids)


    def check(self, music_id):

        music_id   = str(music_id)
        Search_Db  = "NEM" + music_id
        exist_bool = self.r.get(Search_Db)
        if not exist_bool:
            if self.requests_play_url(music_id):
                self.r.set(Search_Db, self.play_url_)
                test.r.expire(Search_Db, 1200)
                # 20分钟更新一轮次
                print("[+]Update!\n")       
            else:
                print("[E] Not Exist play_url\n")
        else:
            print('[-]Exist\n')         

    def requests_play_url(self, music_id):

        post_data      = AES.encrypted_request(self.play_default %(music_id, self.br))
        resp           = self.session.post(url = self.play_url, data = post_data, headers = self.headers)
        resp           = resp.json()
        try:
            self.play_url_   = resp["data"][0]['url']
        except:
            self.play_url_   = None
        if self.play_url_ == None:
            return 0
        else:
            return 1

    def User_SongList(self):
        connection = requests.get(url = "http://music.163.com" + self.User_List_All[1],
                                  headers=self.headers,
                                  )
        connection.encoding = 'UTF-8'
        SongList_Id = re.findall(r'/playlist\?id=(\d+)', connection.text)
        Set_SongList_Id = set(SongList_Id)
        if Set_SongList_Id == []:
            return 0
        return list(Set_SongList_Id)




if __name__ == "__main__":
    test = NEM()
    while(1):
        start = time.time()
        for i in range(0, 21):
            url = 'http://music.163.com'
            url += test.top_list_all[i][1]
            print("Trying -> %s" %url)
            list_ = test.top_songlist(url)
            for z in list_:
                print("Music_Id -> ", z)
                test.check(z)
            time.sleep(0.5)

        for i in test.User_SongList():
            url = 'http://music.163.com/playlist?id='
            url += i
            print("Trying -> %s" %url)
            for z in test.top_songlist(url):
                print("Music_Id -> ", z)
                test.check(z)
            time.sleep(0.5)
        end = time.time() - start
        if end//60 < 20:
            time.sleep(1200 - end)
        # 休眠一定时间后重新更新数据
