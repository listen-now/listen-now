#!usr/bin/env python3
# @File:Scrawl_Xiamimusic.py
# @Date:2018/5/10
# Author:Cat.1

import sys
sys.path.append("..")
import encrypt.xiami_encrypt
import config.config, redis
import requests, re, json


xiami_search_url_first   ='http://api.xiami.com/web?key='
xiami_search_url_index   ='&v=2.0&app_key=1&r=search/songs&page='
xiami_search_url_last    ='&limit=10'
xiami_header             = {
                           'Referer': 'http://m.xiami.com/',
                           'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
                           }
xiami_list_url           = 'http://api.xiami.com/web?v=2.0&app_key=1&id='
xiami_id_url             = 'http://api.xiami.com/web?v=2.0&app_key=1&id='
xiami_dict               = {'hot': 101, 'origin': 103}

requ_date, music_data    = [{} for i in range(2)]

if int(config.config.getConfig("open_database", "redis")) == 1:
    host                 = config.config.getConfig("database", "dbhost")
    port                 = config.config.getConfig("database", "dbport")
    redis_cli            = redis.Redis(host=host, port=int(port), decode_responses=True, db = 2)  

def request_id(music_id):
    url     = "http://www.xiami.com/widget/xml-single/uid/0/sid/%s" %music_id
    headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
                'Referer':'http://www.xiami.com',
                'Content-Type':'application/x-www-form-urlencoded'
                }
    resp            = requests.get(url, headers = headers)
    encrypt_text    = resp.text[resp.text.find("<location><![CDATA[") + len("<location><![CDATA["):resp.text.find("]]></location>")]
    encrypt_content = xiami_encrypt.xiami_encrypt(encrypt_text)
    if check(encrypt_content, music_id):
        return requ_date 

def check(text, music_id):
    regex = re.compile("(^http://$)")
    if not (regex.findall(text[:7])):
        return request_id(music_id)
    else:
        requ_date.update({"playurl":text})
        return 1


class Search_xiami(object):

    def get_search_url(self, music_name, page_num):
        return xiami_search_url_first+music_name+xiami_search_url_index+str(page_num)+xiami_search_url_last

    def search_xiami(self, title, page = 1):
        global requ_date, music_data
        url          = self.get_search_url(title, page)
        c            = requests.get(url = url, headers = xiami_header)
        result       = c.json()
        music_id     = result['data']['songs'][0]['song_id']
        music_name   = result['data']['songs'][0]['song_name']
        artists      = result['data']['songs'][0]['artist_name']
        lyric_url    = result['data']['songs'][0]['lyric']
        image_url    = result['data']['songs'][0]['album_logo']
        play_url     = result['data']['songs'][0]['listen_file']
        regex        = re.compile('<.*?>')
        try:lyric    = requests.get(lyric_url)
        except:lyric = "本首歌还没有歌词!"
        else:lyric   = re.sub(regex, '', lyric.text)
        music_data   = {}
        music_data.update({"play_url":play_url, "music_id": music_id, "music_name": music_name, "artists": artists, "image_url":image_url, "lyric":lyric})
        requ_date.update({'0' : music_data})
        count        = 0
        for i in range(1, 10):
            music_id   = result['data']['songs'][i]['song_id']
            music_name = result['data']['songs'][i]['song_name']
            artists    = result['data']['songs'][i]['artist_name']
            image_url  = result['data']['songs'][i]['album_logo']
            music_data = {}
            count += 1
            music_data.update({"music_id": music_id, "music_name": music_name, "artists": artists, "image_url":image_url})
            requ_date.update({str(count) : music_data})
        return requ_date

    @staticmethod
    def get_music_id(music_id):
        return xiami_id_url + str(music_id)+'&_ksTS=1519879890812_170&callback=jsonp171&r=song/detail'
    
    @staticmethod
    def id_req(music_id):
        url        = Search_xiami.get_music_id(music_id)
        c          = requests.get(url = url, headers = xiami_header)
        result     = c.content.decode()
        result     = json.loads(result[9:-1])
        music_id   = result['data']['song']['song_id']
        music_name = result['data']['song']['song_name']
        artists    = result['data']['song']['artist_name']
        lyric_url  = result['data']['song']['lyric']
        play_url   = result['data']['song']['listen_file']
        image_url  = result['data']['song']['logo']
        regex      = re.compile('<.*?>')
        # print(lyric_url)
        # lyric      = requests.get(lyric_url)
        # lyric      = re.sub(regex, '', lyric.text)
        music_data = {}
        music_data.update({"play_url":play_url, "music_id": music_id, "music_name": music_name, "artists": artists, "image_url":image_url})
        requ_date.update({'0' : music_data})
        return requ_date

def id_search(music_id):
    if request_id(music_id):
        test = Search_xiami()
        Search_xiami.i(music_id)
        return requ_date

if __name__ == '__main__':
    pass
    test = Search_xiami()
    # test.search_xiami('成都', page = 1)
    print(test.id_req(1795575082))
