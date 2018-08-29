#__date__ 2018/7/29
#__file__ KuwoMusic
#__author__ Msc
# encoding:utf-8

import requests
import re
import json
import copy
from project.Module import ReturnStatus
from project.Module import RetDataModule

class KuwoMusic(object):
    '''
        酷我音乐
    '''
    re_dict = copy.deepcopy(RetDataModule.mod_search)
    def __init__(self):
        self.session = requests.Session()
        self.requ_data = {}
        self.search_url = "http://"
        self.play_url = ""
        self.url = ""
        self.comment_url = ""
        self.lyric_url = ""
        self.session = requests.session()
        self.header = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Host':'antiserver.kuwo.cn',
        'Range': 'bytes=0-',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':base_url
        }
    
    def search_by_key_word(self,keyword,page=1,num=10):
        '''
            keyword=需要搜索的歌曲或歌手
            page=查询的页码数
            num=当前页的返回数量
        '''

        try:
            _url = "http://search.kuwo.cn/r.s?all={0}&ft=music&itemset=web_2013&client=kt&pn={1}&rn={2}&rformat=\
                json&encoding=utf8".format(keyword,page,num)
            response = self.session.request('GET',_url,hearder = self.headers)
            serach_res = response.json()
            if serach_res.get('code', -1) == 0:
                song_list = serach_res.get('data',{}).get('song',{}).get('list',[])
                for music in song_list:
                    tmp_song = copy.deepcopy(RetDataModule.mod_song) #拷贝歌曲模板
                    music_id = music['mid']
                    tmp_song['music_id'] = music_id
                    tmp_song['play_url'] = self.get_play_url(music_id)
                    tmp_song['music_name'] = music['name']
                    tmp_song['artists'] = music['singer'][0]['name']
                    tmp_song['image_url'] = self.get_image_url(music_id)
                    tmp_song['lyric'] = self.get_music_lyric(music_id)
                    re_dict['song']['list'].append(copy.deepcopy(tmp_song)) #添加到歌曲列表
                    re_dict['song']['totalnum'] += 1
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict

    def get_play_url(self,music_id):
        return "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={0}&format=aac|mp3&response=url".format(music_id)

    def get_play_lyric(self,lyric):
        pass
    def get_image_url(self,mvpic):
        pass



