# -*- coding: utf-8 -*-
# __date__ 2018/7/29
# __file__ KuwoMusic
# __author__ Msc


import simplejson
from project.Module import ReturnStatus
from project.Module import RetDataModule
from project.Module import ReturnFunction
import requests
import copy
import json
import demjson

class KuwoMusic(object):
    '''
        酷我音乐
    '''
    
    global null
    null=''
    re_dict = copy.deepcopy(RetDataModule.mod_search)
    def __init__(self):
        self.baseurl = "http://search.kuwo.cn/r.s?all=%s&ft=music&itemset=web_2018&client=kt&pn=%s&rn=10&rformat=json&encoding=utf8"
        self.searchurl = "http://m.kuwo.cn/newh5/singles/songinfoandlrc?musicId=%s"
        self.palyurl = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid=%s&format=aac|mp3&response=url"
        self.commenturl = "http://comment.kuwo.cn/com.s?type=get_comment&uid=0&prod=newWeb&digest=15&sid=%s&page=1&rows=10&f=web"
        self.session = requests.session()
        self.headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }

    def Search_List(self, keyword, page):

        re_dict = copy.deepcopy(RetDataModule.mod_search)

        try:
            resp = eval(self.session.get(url=self.baseurl%(keyword, page), headers=self.headers).text)

        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
            
        if resp["HIT"] != 0 :
            songList = ReturnFunction.songList(Data=resp["abslist"], songdir="[\"SONGNAME\"]",artistsdir="[\"ARTIST\"]",iddir="[\"MUSICRID\"][6:]")
            songList.buidingSongList()
            re_dict_class = ReturnFunction.RetDataModuleFunc()
            now_page      = page + 1
            before_page, next_page = page , page +2
            totalnum      = songList.count
            re_dict       = re_dict_class.RetDataModSearch(now_page, next_page, before_page, songList, totalnum, code=ReturnStatus.SUCCESS, status='Success')
            
            return re_dict



    def Search_details(self,music_id):

        try:
            resp = eval(self.session.get(url=self.searchurl%(music_id),headers=self.headers).text)
        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
            return 0
        else:
            code   = ReturnStatus.SUCCESS
            status = "ReturnStatus.SUCCESS"

            try:
                resp = resp["data"]
                re_dict_class = ReturnFunction.RetDataModuleFunc()
                re_dict = re_dict_class.RetDataModSong(self.get_play_url(music_id), resp["songinfo"]["id"], resp["songinfo"]['songName'], 
                    resp["songinfo"]['artist'], resp["songinfo"]['pic'], resp['lrclist'], self.get_comment(music_id), tlyric='None', 
                    code=code, status=status)
            
            except:re_dict["code"]    = ReturnStatus.DATA_ERROR
        return re_dict


    def get_play_url(self,music_id):
        re_dict = copy.deepcopy(RetDataModule.mod_song)

        play_url = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={0}&format=aac|mp3&response=url".format(music_id)
        return play_url


    def get_comment(self,music_id):
        resp = eval(self.session.get(url=self.commenturl%(music_id),headers=self.headers).text)
        comment = resp["rows"]
        return comment




if __name__=="__main__":

    test = KuwoMusic()

    rest.Search_List("青花瓷",0)