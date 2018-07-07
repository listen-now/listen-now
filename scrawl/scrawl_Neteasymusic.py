#!/usr/bin/env python3
# @File:Scrawl_Neteasymusic.py
# @Date:2018/5/9
# Author:Cat.1


import requests, re, json
import sys
sys.path.append("..")
import encrypt.AES
import time, datetime, base64
import urllib.parse
import redis
import config.config
import threading
import queue



class Netmusic(object):


    def __init__(self):
        self.requ_date    = {}
        self.search_url   = "http://music.163.com/api/search/get/web?csrf_token="
        # 通过歌曲名称获得歌曲的ID信息(GET请求)
        self.play_url     = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
        # 通过加密数据POST请求得到播放地址
        # https://api.imjad.cn/cloudmusic/?type=song&id=%s&br=320000
        self.url_         = "http://music.163.com/song/media/outer/url?id=%s.mp3"
        # 网易根据api直接请求到下载音乐地址(%s均为歌曲id)
        self.comment_url  = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token="
        # 通过加密数据POST请求得到评论内容        
        self.lyric_url    = "http://music.163.com/api/song/lyric?id=%s&lv=1&kv=1&tv=-1"      
        # 通过id获得歌曲的歌词信息(json包) 只需要(GET请求)
        self.session      = requests.session()
        self.headers      = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Referer':'http://music.163.com/',
        'Content-Type':'application/x-www-form-urlencoded'
        }
        self.play_default = "{\"ids\":\"[%s]\",\"br\":%s\
        ,\"csrf_token\":\"\"}"
        if int(config.config.getConfig("open_database", "redis")) == 1:
            host              = config.config.getConfig("database", "dbhost")
            port              = config.config.getConfig("database", "dbport")
            self.r            = redis.Redis(host=host, port=int(port), decode_responses=True)  
        self.br           = "128000"

    def new_requests_play_url(self, music_id):
        global music_data
        new_music_id     = []

        if int(config.config.getConfig("open_database", "redis")) == 1:    
            Search_Db        = "NEM" + str(music_id)
            exist_bool       = self.r.get(Search_Db)
            if not exist_bool:
                play_url = self.url_ %(music_id)
                self.r.set(Search_Db, play_url)
            else:
                play_url     = exist_bool
                new_music_id = re.findall(r"url\?id=(\d{1,20})", exist_bool)        
        else:
            play_url = self.url_ %(music_id)
        music_data = {}
        try:
            music_data.update({"play_url": play_url, "music_id":music_id[0]})
        except:
            music_data.update({"play_url": play_url, "music_id":music_id})            
        try:            
            self.requ_date["0"].update(music_data)
        except:
            self.requ_date.update({"0":music_data})


    def requests_play_url(self, music_id, proxies=''):
        self.post_data = AES.encrypted_request(self.play_default %(music_id, self.br))
        if proxies == '':
          resp           = self.session.post(url=self.play_url, data=self.post_data, headers=self.headers)
        else:
          resp           = self.session.post(url=self.play_url, data=self.post_data, headers=self.headers, proxies=proxies)
        try:
            resp         = resp.json()
        except:
            host       = config.config.getConfig("database", "dbhost")
            port       = config.config.getConfig("database", "dbport")
            self.r     = redis.Redis(host=str(host),port=int(port),db=4)
            random_int = random.sample(range(0, self.r.dbsize()), 1)
            proxies    = self.r.get(str(random_int[0]))
            self.requests_play_url(music_id, eval(proxies))
        play_url       = resp["data"][0]['url']
        if play_url == None:
            play_url = self.url_ %(music_id)
        self.requ_date['0'] = {}        
        self.requ_date['0'].update({"play_url": play_url})

    def requests_comment(self, music_id, proxies=''):
        if proxies == '':
          resp         = self.session.post(url=self.comment_url %(music_id), data=self.post_data, headers=self.headers)
        else:
          resp         = self.session.post(url=self.comment_url %(music_id), data=self.post_data, headers=self.headers, proxies=proxies)
        try:
            resp       = resp.json()
        except:
            host       = config.config.getConfig("database", "dbhost")
            port       = config.config.getConfig("database", "dbport")
            self.r     = redis.Redis(host=str(host),port=int(port),db=4)
            random_int = random.sample(range(0, self.r.dbsize()), 1)
            proxies    = self.r.get(str(random_int[0]))
            self.requests_comment(music_id, eval(proxies))
        try:
            self.like              = resp["hotComments"][0]["likedCount"]
            self.username          = resp["hotComments"][0]['user']["nickname"]
            self.comment_content   = resp["hotComments"][0]["content"]
            self.comment_timestamp = int(str(resp["hotComments"][0]["time"])[:-3])
            dateArray              = datetime.datetime.utcfromtimestamp(self.comment_timestamp)
            self.comment_time      = dateArray.strftime("%Y--%m--%d %H:%M:%S")
            self.requ_date['0'].update({"comment_time": self.comment_time, "comment_content":self.comment_content, "likecount":self.like, "username":self.username})
        except:
            self.requ_date['0'].update({"detail":"本首歌曲还没有评论~"})
    def music_id_requests(self, music_id):
        t1 = threading.Thread(target=self.new_requests_play_url, args=(music_id,))
        # self.new_requests_play_url 的异步请求
        t2 = threading.Thread(target=self.requests_lyric, args=(music_id,))
        # self.requests_lyric        的异步请求
        t3 = threading.Thread(target=self.music_detail, args=(music_id,))

        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        music_id = self.requ_date['0']["music_id"]
        # self.requests_play_url(music_id)
        # 切换到速度较快的备用模式
        # self.requests_comment(music_id)
        return self.requ_date
    
    def music_detail(self, music_id, _update="0", proxies=''):
        url        = "http://music.163.com/api/song/detail?ids=[%s]"
        if proxies == '':
          resp         = self.session.get(url=url %music_id, headers=self.headers)
        else:
          resp         = self.session.get(url=url %music_id, headers=self.headers, proxies=proxies)
        try:
            content    = resp.json()
        except:
            host       = config.config.getConfig("database", "dbhost")
            port       = config.config.getConfig("database", "dbport")
            self.r     = redis.Redis(host=str(host),port=int(port),db=4)
            random_int = random.sample(range(0, self.r.dbsize()), 1)
            proxies    = self.r.get(str(random_int[0]))
            self.music_detail(music_id, eval(proxies))

        name       = content['songs'][0]["name"]
        artists    = content['songs'][0]["artists"][0]["name"]
        image_url  = content['songs'][0]["album"]["picUrl"]
        music_data = {}
        music_data.update({"image_url":image_url, "music_name":name, "artists":artists})
        try:
            self.requ_date[_update].update(music_data)
        except:    
            self.requ_date[_update] = {}
            self.requ_date[_update].update(music_data)

        return self.requ_date

    def pre_response_neteasymusic(self, text, page = 1):
        global count, i, lock

        text       = urllib.parse.quote(text)                        
        data       = "hlpretag=&hlposttag=&s=%s&type=1&offset=0&total=true&limit=100" %(text)
        resp       = self.session.post(url = self.search_url, data = data, headers = self.headers)
        result     = resp.json()

        try:
            if page == 1:
                music_id      = result['result']['songs'][0]['id']
                # music_data    = {}
                self.music_detail(music_id)

                # music_name    = result['result']['songs'][0]['name']
                # artists       = result['result']['songs'][0]['artists'][0]['name']
                # music_data.update({"music_id": music_id, "music_name":music_name, "artists":artists})
                # self.requ_date['0'].update(music_data)
            else:
                music_id      = result['result']['songs'][page * 2 - 9]['id']
                music_name    = result['result']['songs'][page * 2 - 9]['name']
                artists       = result['result']['songs'][page * 2 - 9]['artists'][0]['name']
                music_data    = {}
                music_data.update({"music_id": music_id, "music_name": music_name, "artists": artists})
                self.requ_date.update({'0' : music_data})
            page_end   = page * 10
            page_start = page_end - 9
            if page != 1:
                page_start = page_end - 8
            q = queue.Queue()
            i = page_start
            count = 1
            while(i<page_end):
                music_data    = {}
                music_id_2    = result['result']['songs'][i]['id']
                music_name_2  = result['result']['songs'][i]['name']
                artists_2     = result['result']['songs'][i]['artists'][0]['name']
                Search_Db     = "NEM" + str(music_id_2)
                exist_bool    = self.r.get(Search_Db)   
                if not exist_bool :
                    play_url = self.url_ %(music_id_2)
                    self.r.set(Search_Db, play_url)
                else:
                    play_url = exist_bool
                music_data.update({"music_id": music_id_2, "play_url":play_url, "artists":artists_2, "music_name":music_name_2})                    
                try:
                    self.requ_date[str(count)].update(music_data)
                except KeyError:
                    self.requ_date[str(count)] = {}
                    self.requ_date[str(count)].update(music_data)
                count += 1
                i     += 1


        except EOFError:
            try:
                music_id   = result['result']['songs'][0]['id']
                music_name = result['result']['songs'][0]['name']
                artists    = result['result']['songs'][0]['artists'][0]['name']
            except:
                print("[-]Platform not The music")
                return 0
                # 该平台上没有该音乐任何信息!
            else:
                self.requ_date.update({"music_id":music_id, "music_name":music_name, "artists":artists})
                # 返回首备选歌曲信息.
                t1 = threading.Thread(target=self.new_requests_play_url, args=(music_id,))
                # self.new_requests_play_url 的异步请求
                t2 = threading.Thread(target=self.requests_lyric, args=(music_id,))
                # self.requests_lyric        的异步请求
                t1.start()
                t2.start()
                t1.join()
                t2.join()

                music_id = self.requ_date["music_id"]
                # self.requests_play_url(music_id)
                # self.requests_comment(music_id)
                return self.requ_date
                # 处理首备选歌曲
        else:
            t1 = threading.Thread(target=self.new_requests_play_url, args=(music_id,))
            # self.new_requests_play_url 的异步请求
            t2 = threading.Thread(target=self.requests_lyric, args=(music_id,))
            # self.requests_lyric        的异步请求
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            # self.requests_play_url(music_id)
            # self.requests_comment(music_id)
            return self.requ_date

            # 只返回第一首备选歌曲的详细信息.

    def requests_lyric(self, music_id):
        self.lyric_data  = self.session.get(url = self.lyric_url %(music_id), headers = self.headers)
        try:self.lyric   = self.lyric_data.json()["lrc"]["lyric"]
        except: self.lyric = {"本首歌还没有歌词!"}
        else:
            music_data = {}
            music_data.update({"lyric": self.lyric})
            self.requ_date['0'].update(music_data)

            try: self.tlyric = self.lyric_data.json()["tlyric"]["lyric"]
            except: 
                pass
            else:
                music_data = {}
                music_data.update({"tlyric": self.tlyric})
                self.requ_date['0'].update(music_data)
        return 1


if __name__ == '__main__':
    test = Netmusic()
    # print(test.music_id_requests(444706287))
    print(test.pre_response_neteasymusic('大鱼'))
    # test.pre_response_neteasymusic('大鱼')
