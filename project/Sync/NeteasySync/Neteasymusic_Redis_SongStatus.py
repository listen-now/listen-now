#!usr/bin/env python3
# @File:Neteasymusic_Redis_SongStatus.py
# @Date:2018/05/20
# Author:Cat.1

import redis, time
import requests, re
from requests import RequestException
from project.Sync.NeteasySync.encrypt import AES
from project.Config import config


class NEM(object):
    """
    这是用于维护redis中网易云音乐的音乐地址的可用性的类
    通常他会持续更新云音乐中的歌曲链接放入redis
    利用redis的高效率来实现服务器快速反应, 降低反应延迟
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
        self.r       = redis.Redis(host=host, port=int(port), decode_responses=True)  
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
        """
        这是用来下载top_songlist的热门排行版的方法
        """
        try:
            connection = requests.get(url = url,
                                      headers=self.headers,
                                      )
        except:
            return 0
        else:
            connection.encoding = 'UTF-8'
            songids = re.findall(r'/song\?id=(\d+)', connection.text)
            songids = set(songids)
            if songids == []:
                return 0
            return list(songids)


    def check(self, music_id):
        """
        这是用来检测redis中是否有该歌曲的链接的方法
        其中网易音乐在redis中的命名方式是 NEM + music_id
        例如 : NEM123456
        """
        music_id   = str(music_id)
        Search_Db  = "NEM" + music_id
        exist_bool = self.r.get(Search_Db)
        if not exist_bool:
            # if self.requests_play_url(music_id):
            self.url_           = "http://music.163.com/song/media/outer/url?id=%s.mp3" %music_id
            self.r.set(Search_Db, self.url_)
                # 20分钟更新一轮次
            print("[+]Update!\n")       
        else:
            print('[-]Exist\n')         

    def requests_play_url(self, music_id):
        """
        这是用于请求网易云音乐歌曲地址的方法
        他调用了加密方式是外部编写的AES文件
        """
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
        """
        这是用于获取用户热门歌单的歌曲地址的方法
        """
        try:
            connection = requests.get(url = "http://music.163.com" + \
                                      self.User_List_All[1],
                                      headers=self.headers,
                                      )
        except:
            return 0
        else:
            connection.encoding = 'UTF-8'
            SongList_Id         = re.findall(r'/playlist\?id=(\d+)', \
                                             connection.text)
            Set_SongList_Id     = set(SongList_Id)
            if Set_SongList_Id == []:
                return 0
            return list(Set_SongList_Id)




if __name__ == "__main__":

    """
    这里是形成死循环, 不断更新网易音乐的歌曲地址
    为什么要更新?
    因为歌曲地址都带有时间, 长期会失效
    第一个for循环是更新排行榜
    第二个for循环是更新用户热门歌单
    """
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
        time.sleep(12 * 3600)
        # if end//60 < 20:
        #     time.sleep(1200 - end)
        # 休眠一定时间后重新更新数据
