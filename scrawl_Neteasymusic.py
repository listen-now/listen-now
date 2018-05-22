#coding=utf-8
#!usr/bin/env python3
# @File:Scrawl.py
# @Date:2018/5/9
# Author:Cat.1
import requests, re, json
import AES
import time, datetime, base64
import urllib.parse
import redis
import config
class Netmusic(object):

    def __init__(self):
        self.requ_date = {}
        self.search_url   = "http://music.163.com/api/search/get/web?csrf_token="
        self.play_url     = "http://music.163.com/weapi/song/enhance/player/url?csrf_token="
        # https://api.imjad.cn/cloudmusic/?type=song&id=%s&br=320000
        self.url_         = "http://music.163.com/song/media/outer/url?id=%s.mp3"
        self.comment_url  = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token="
        self.lyric_url    = "http://music.163.com/api/song/lyric?id=%s&lv=1&kv=1&tv=-1"      
        self.session      = requests.session()
        self.headers      = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
        'Referer':'http://music.163.com/',
        'Content-Type':'application/x-www-form-urlencoded'
        }
        self.play_default = "{\"ids\":\"[%s]\",\"br\":%s\
        ,\"csrf_token\":\"\"}"
        host = config.getConfig("database", "dbhost")
        port = config.getConfig("database", "dbport")
        self.r       = redis.Redis(host=host, port=int(port), decode_responses=True)  
        self.br           = "128000"

    def new_requests_play_url(self, music_id):
        # self.post_data = AES.encrypted_request(self.play_default %(music_id, self.br))
        Search_Db  = "NEM" + str(music_id)
        exist_bool = self.r.get(Search_Db)
        if not exist_bool:
            play_url = self.url_ %(music_id)
            self.r.set(Search_Db, play_url)
        else:
            play_url = exist_bool
        try:
            self.requ_date['0'].update({"play_url": play_url})
        except:
            self.requ_date['0'] = {}
            self.requ_date['0'].update({"play_url": play_url})

    def requests_play_url(self, music_id):
        
        self.post_data = AES.encrypted_request(self.play_default %(music_id, self.br))
        resp           = self.session.post(url = self.play_url, data = self.post_data, headers = self.headers)
        resp           = resp.json()
        play_url       = resp["data"][0]['url']
        if play_url == None:
            play_url = self.url_ %(music_id)
        self.requ_date['0'] = {}        
        self.requ_date['0'].update({"play_url": play_url})

    def requests_comment(self, music_id):
        resp                   = self.session.post(url = self.comment_url %(music_id), data = self.post_data, headers = self.headers)
        resp                   = resp.json()
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
        self.new_requests_play_url(music_id)
        # self.requests_play_url(music_id)
        # self.requests_comment(music_id)
        self.requests_lyric(music_id)
        return self.requ_date

    def pre_response_neteasymusic(self, text, page = 1):
        text       = urllib.parse.quote(text)                        
        data       = "hlpretag=&hlposttag=&s=%s&type=1&offset=0&total=true&limit=100" %(text)
        resp       = self.session.post(url = self.search_url, data = data, headers = self.headers)
        result     = resp.json()
        try:
            if page == 1:
                music_id      = result['result']['songs'][0]['id']
                music_name    = result['result']['songs'][0]['name']
                artists       = result['result']['songs'][0]['artists'][0]['name']
                music_data    = {}
                music_data.update({"music_id": music_id, "music_name": music_name, "artists": artists})
                self.requ_date.update({'0' : music_data})
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
            count = 1
            for i in range(page_start, page_end+1):
                music_data    = {}
                music_id_2    = result['result']['songs'][i]['id']
                music_name_2  = result['result']['songs'][i]['name']
                artists_2     = result['result']['songs'][i]['artists'][0]['name']
                Search_Db     = "NEM" + str(music_id_2)
                exist_bool    = self.r.get(Search_Db)
                
                if not exist_bool :
                    play_url = self.url_ %(music_id)
                    self.r.set(Search_Db, play_url)
                else:
                    play_url = exist_bool
                music_data.update({"music_id": music_id_2, "music_name": music_name_2, "artists": artists_2, "play_url":play_url})
                self.requ_date.update({str(count) : music_data})
                count += 1
        except EOFError:
            try:
                music_id   = result['result']['songs'][0]['id']
                music_name = result['result']['songs'][0]['name']
                artists    = result['result']['songs'][0]['artists'][0]['name']
            except:
                print("[-]Platform not The music")
                return 0
            else:
                self.requ_date.update({"music_id":music_id, "music_name":music_name, "artists":artists, })
                # 返回首备选歌曲信息.
                self.new_requests_play_url(music_id)
                # self.requests_play_url(music_id)
                # self.requests_comment(music_id)
                self.requests_lyric(music_id)
                return self.requ_date
        else:
            # result songs 0-5 id name artists
            self.new_requests_play_url(music_id)
            # self.requests_play_url(music_id)
            # self.requests_comment(music_id)
            self.requests_lyric(music_id)
            return self.requ_date


    def requests_lyric(self, music_id):
        self.lyric_data  = self.session.get(url = self.lyric_url %(music_id), headers = self.headers)
        try:self.lyric   = self.lyric_data.json()["lrc"]["lyric"]
        except: self.lyric = {"本首歌还没有歌词!"}
        else:
            self.requ_date['0'].update({"lyric": self.lyric})
            try: self.tlyric = self.lyric_data.json()["tlyric"]["lyric"]
            except: 
                pass
            else: 
                self.requ_date['0'].update({"tlyric": self.tlyric})
            # print(self.requ_date)
        return 1

if __name__ == '__main__':
    test = Netmusic()
    # print(test.music_id_requests(444706287))
    print(test.pre_response_neteasymusic('白金迪斯科'))
