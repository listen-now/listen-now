# -*- coding: utf-8 -*-
# __date__: 2018/8/31
# __file__: MiguMusic
# __author__: Msc

import simplejson
from project.Module import ReturnStatus
from project.Module import RetDataModule
from project.Module import ReturnFunction
import requests
import copy
import json


class Migu(object):
    '''
        migumusic scrawl
    '''
    global null
    null=''
    re_dict = copy.deepcopy(RetDataModule.mod_search)
    def __init__(self):
        self.session = requests.session()
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept': 'application/json, text/js, */*; q=0.01',
        }
        self.searchurl = 'http://m.music.migu.cn/migu/remoting/scr_search_tag?rows=10&type=2&keyword=%s&pgc=%s'
        self.detailurl = 'http://m.music.migu.cn/migu/remoting/cms_detail_tag?c=5108&cpid=%s'


    def search(self, keyword, page):

        re_dict = copy.deepcopy(RetDataModule.mod_search)
        try:
            response1 = self.session.request('GET',url=self.searchurl%(keyword, page), headers=self.headers)
            resp = response1.json() 
            if resp["pgt"] != 0 :
                song_list = resp.get('data',{}).get('song',{}).get('list',[])
                songList = ReturnFunction.songList(Data=song_list["musics"], songdir="[\"songName\"]",artistdir="[\"singerName\"]",iddir="[\"copyrightId\"]")
                songList.buidingSongList()
                re_dict_class = ReturnFunction.RetDataModuleFunc()
                now_page      = page
                before_page, next_page = page-1, page+1
                totalnum      = songList.count
                re_dict       = re_dict_class.RetDataModSearch(now_page, next_page, before_page, songList, totalnum, code=ReturnStatus.SUCCESS, status='Success')
                return re_dict
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
                re_dict['status'] = 'ERROR_SEVER'

        except simplejson.errors.JSONDecodeError :
            re_dict["code"] = ReturnStatus.ERROR_SEVER
        

    def search_details(self,music_id):
        re_dict = copy.deepcopy(RetDataModule.mod_song)
        try:
            resp = eval(self.session.get(url=self.detailurl%(music_id),headers=self.headers).text)
        except simplejson.errors.JSONDecodeError:
            re_dict["code"] = ReturnStatus.ERROR_SEVER
            return re_dict

        try:
            re_dict["music_id"] = resp["data"]["songId"]
            re_dict["music_name"] = resp["data"]["songName"]
            re_dict["artists"] = resp["data"]["singerName"]
            re_dict["play_url"] = resp['data']['listenUrl']
            re_dict["lyric"] = resp["data"]["lyricLrc"]
            re_dict["image_url"] = resp["data"]["picL"]
            #re_dict["comment"] = 
        except:
            re_dict["code"]    = ReturnStatus.DATA_ERROR
        else:
            re_dict["code"]      = ReturnStatus.SUCCESS
        
        return re_dict

    # def search_list(self, list_id):
    #     re_dict              = copy.deepcopy(RetDataModule.mod_cdlist)
        


if __name__=="__main__":

    test = Migu()

    rest.search("怪咖",1)




