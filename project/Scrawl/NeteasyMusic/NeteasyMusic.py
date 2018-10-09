#!/usr/bin/env python3
# @File:Scrawl_Neteasymusic.py
# @Date:2018/5/9
# Author:Cat.1

import requests, re, json
from .NeteasyHelper import AES #同级目录用.表示
import time, datetime, base64
import urllib.parse
import redis
from project.Config import config #从项目包顶导入
import threading
import queue
from project.Module import ReturnStatus
from project.Module import RetDataModule
from project.Module import ReturnFunction


class Netmusic(object):


    def __init__(self):
        self.requ_date    = {"song":{"totalnum":"", "list":[{}]}}

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
        if int(config.getConfig("open_database", "redis")) == 1:
            host   = config.getConfig("database", "dbhost")
            port   = config.getConfig("database", "dbport")
            self.r = redis.Redis(host=host, port=int(port), decode_responses=True)  
        self.br    = "128000"

    def new_requests_play_url(self, music_id):
        global music_data
        new_music_id = []

        if int(config.getConfig("open_database", "redis")) == 1:    
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

        return play_url



    def requests_play_url(self, music_id, proxies=''):
        self.post_data = AES.encrypted_request(self.play_default %(music_id, self.br))
        if proxies == '':
          resp           = self.session.post(url=self.play_url, data=self.post_data, headers=self.headers)
        else:
          resp           = self.session.post(url=self.play_url, data=self.post_data, headers=self.headers, proxies=proxies)
        try:
            resp         = resp.json()
        except:
            host       = config.getConfig("database", "dbhost")
            port       = config.getConfig("database", "dbport")
            self.r     = redis.Redis(host=str(host),port=int(port),db=5)
            random_int = random.sample(range(0, self.r.dbsize()), 1)
            proxies    = self.r.get(str(random_int[0]))
            self.requests_play_url(music_id, eval(proxies))
        play_url       = resp["data"][0]['url']
        if play_url == None:
            play_url = self.url_ %(music_id)
        self.requ_date["song"]["list"][0].update({"play_url": play_url})



    def requests_comment(self, music_id, proxies=''):
        if proxies == '':
            self.post_data = AES.encrypted_request(self.play_default %(music_id, self.br))
            resp         = self.session.post(url=self.comment_url %(music_id), data=self.post_data, headers=self.headers)
        else:
            resp         = self.session.post(url=self.comment_url %(music_id), data=self.post_data, headers=self.headers, proxies=proxies)
        try:
            resp       = resp.json()
        except:
            host       = config.getConfig("database", "dbhost")
            port       = config.getConfig("database", "dbport")
            self.r     = redis.Redis(host=str(host),port=int(port),db=4)
            random_int = random.sample(range(0, self.r.dbsize()), 1)
            proxies    = self.r.get(str(random_int[0]))
            self.requests_comment(music_id, eval(proxies))
        self.requ_date["song"]["comments"] = []

        for item in resp["hotComments"]:
            like              = item["likedCount"]
            username          = item['user']["nickname"]
            comment_content   = item["content"]
            comment_timestamp = int(str(item["time"])[:-3])
            dateArray         = datetime.datetime.utcfromtimestamp(comment_timestamp)
            comment_time      = dateArray.strftime("%Y--%m--%d %H:%M:%S")
            self.requ_date["song"]["comments"].append({"comment_time":comment_time, "comment_content":comment_content, "likecount":like, "username":username})
        return self.requ_date["song"]["comments"]

    def music_id_requests(self, music_id):


        id_flag        = 1
        musicDataiList = self.music_detail(music_id, id_flag)
        
        lyric          = self.requests_lyric(music_id)
        re_dict_class  = ReturnFunction.RetDataModuleFunc()
        re_dict        = re_dict_class.RetDataModSong(self.new_requests_play_url(music_id), music_id,
                            musicDataiList['music_name'], musicDataiList['artists'], musicDataiList['image_url'], 
                            lyric['lyric'], comment=self.requests_comment(music_id),
                            tlyric=lyric['tlyric'], code=ReturnStatus.SUCCESS, status='Success')

        return re_dict
    
    def music_detail(self, music_id, id_flag=0, proxies=''):
        music_data = {}
        url        = "http://music.163.com/api/song/detail?ids=[%s]"
        if proxies == '':
          resp         = self.session.get(url=url %music_id, headers=self.headers)
        else:
          resp         = self.session.get(url=url %music_id, headers=self.headers, proxies=proxies)
        try:
            content    = resp.json()
        except:
            host       = config.getConfig("database", "dbhost")
            port       = config.getConfig("database", "dbport")
            self.r     = redis.Redis(host=str(host),port=int(port),db=4)
            random_int = random.sample(range(0, self.r.dbsize()), 1)
            proxies    = self.r.get(str(random_int[0]))
            self.music_detail(music_id, eval(proxies))
        try:
            name       = content['songs'][0]["name"]
            artists    = content['songs'][0]["artists"][0]["name"]
            image_url  = content['songs'][0]["album"]["picUrl"]
        except:
            music_data['code'] = ReturnStatus.ERROR_SEVER
        else:
            
            music_data.update({"image_url":image_url, "music_name":name, "artists":artists})
            try:
                if id_flag == 1:
                    self.requ_date["song"]["list"][0].update(music_data)
                try:
                    self.requ_date["song"]["list"][0]["image_url"]
                except KeyError:
                    self.requ_date["song"]["list"][0].update(music_data)
                else:
                    self.requ_date["song"]["list"].append(music_data)
            except:
                self.requ_date["song"]["list"] = {}
                self.requ_date["song"]["list"].append(music_data)
        return self.requ_date["song"]["list"][0]



    def pre_response_neteasymusic(self, text, page = 1):
        global count, i, lock

        text       = urllib.parse.quote(text)                        
        data       = "hlpretag=&hlposttag=&s=%s&type=1&offset=%s&total=true&limit=10" %(text, str((page-1)*10))
        resp       = self.session.post(url = self.search_url, data = data, headers = self.headers)
        result     = resp.json()
        try:
            songList      = ReturnFunction.songList(Data=result['result']['songs'], songdir="[\"name\"]", artistsdir="[\'artists\'][0][\'name\']", iddir="[\"id\"]", page=page)
            songList.buidingSongList()
            re_dict_class = ReturnFunction.RetDataModuleFunc()
            now_page      = page
            before_page, next_page = page-1, page+1
            totalnum      = songList.count
            re_dict       = re_dict_class.RetDataModSearch(now_page, next_page, before_page, songList, totalnum, code=ReturnStatus.SUCCESS, status='Success')
        except KeyError:
            code   = ReturnStatus.NO_EXISTS
            status = 'ReturnStatus.NO_EXISTS'
            return ReturnStatus.NO_EXISTS

        except:
            code   = ReturnStatus.ERROR_UNKNOWN
            status = 'ReturnStatus.ERROR_UNKNOWN'
            return ReturnStatus.ERROR_UNKNOWN
        else:
            re_dict['code']   = ReturnStatus.SUCCESS
            re_dict['status'] = 'ReturnStatus.SUCCESS'
            return re_dict



    def requests_lyric(self, music_id):
        self.lyric_data  = self.session.get(url = self.lyric_url %(music_id), headers = self.headers)
        self.lyric  = self.lyric_data.json()["lrc"].get("lyric", "本首歌还没有歌词")
        self.tlyric = self.lyric_data.json()["tlyric"].get("lyric", "None")

        return {"lyric":self.lyric, "tlyric":self.tlyric}


if __name__ == '__main__':
    test = Netmusic()
    print(test.music_id_requests(444706287))
    # print(test.pre_response_neteasymusic('大鱼'))
    # test.pre_response_neteasymusic('大鱼')





