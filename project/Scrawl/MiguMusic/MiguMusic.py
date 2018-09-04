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
        self.songlisturl = 'http://m.music.migu.cn/migu/remoting/playlistcontents_query_tag?playListType=2&playListId=%s'
        self.createUserurl = 'http://m.music.migu.cn/migu/remoting/playlist_query_tag?onLine=1&queryChannel=0&createUserId=%s=&contentCountMin=5&playListId=%s'

    def search(self, keyword, page):

        re_dict = copy.deepcopy(RetDataModule.mod_search)
        
        try:
            resp = self.session.get(url=self.searchurl%(keyword, page), headers=self.headers)
            resp = resp.json()

        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"

        if resp["pgt"] != 0 :
            songList = ReturnFunction.songList(Data=resp["musics"], songdir="[\"songName\"]",artistsdir="[\"artist\"]",iddir="[\"copyrightId\"]")
            songList.buidingSongList()
            re_dict_class = ReturnFunction.RetDataModuleFunc()
            now_page      = page 
            before_page, next_page = page -1 , page +1
            totalnum      = songList.count
            re_dict       = re_dict_class.RetDataModSearch(now_page, next_page, before_page, songList, totalnum, code=ReturnStatus.SUCCESS, status='Success')
            
            return re_dict

    
    def search_details(self,music_id):
        try:
            resp = eval(self.session.get(url=self.detailurl%(music_id),headers=self.headers).text)
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
                re_dict = re_dict_class.RetDataModSong(resp["listenUrl"], resp["songId"], str(resp["songName"]), 
                    str(resp["singerName"])[2:-2], resp["picL"], resp["lyricLrc"], comment=[], tlyric='None', code=code, status=status)
            
            except:re_dict["code"]    = ReturnStatus.DATA_ERROR
        return re_dict

    # def search_songlist(self, listid):
    #     try:
    #         resp = eval(self.session.get(url=self.songlisturl%(listid),headers=self.headers).text)
    #     except simplejson.errors.JSONDecodeError:
    #         code   = ReturnStatus.ERROR_SEVER
    #         status = "ReturnStatus.ERROR_SEVER"
    #         return 0
    #     else:
    #         code   = ReturnStatus.SUCCESS
    #         status = "ReturnStatus.SUCCESS"
    #         try:
    #             re_dict_class = ReturnFunction.RetDataModuleFunc()
    
    #             songList = ReturnFunction.songList(Data=resp["contentList"], songdir="[\"contentName\"]", artistsdir="[\'singerName\']", iddir="[\"songId\"]")
    #             songList.buidingSongList()
                # re_dict  = re_dict_class.RetDataModCdlist(resp["contentList"]['specialname'], 
                #                                          resp['info']['list']['nickname'], resp['info']['list']['intro'], 
                #                                          resp['info']['list']['specialid'], image.replace(r"{size}", "400"), 
                #                                          songList, resp['list']['list']['total'], resp['list']['list']['total'], 
                #                                          code=code, status=status)

if __name__=="__main__":

    test = Migu()

    rest.search("怪咖",1)




