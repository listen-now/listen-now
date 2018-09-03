#!/usr/bin/env python3
# @File:kugou.py
# @Date:2018/08/01
# Author:Cat.1    

# # encoding:utf-8
# import io  
# import sys  
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 
import copy
import requests
import simplejson
from project.Module import ReturnStatus
from project.Module import RetDataModule
from project.Module import ReturnFunction

class Kugou(object):


    def __init__(self):

        self.baseurl = "http://mobilecdn.kugou.com/api/v3/search/song?format=jsonp&keyword=%s&page=%s&pagesize=10&showtype=1&callback=kgJSONP557904816"
        # 用于搜索并且获取hash的api
        self.hashurl = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s"
        self.session = requests.session()
        self.headers = {
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/603.1.13 (KHTML, like Gecko) Version/10.1 Safari/603.1.13',
                        'Referer':'http://mobilecdn.kugou.com/'
                        }


    def Search_List(self, keyword, page=1) -> str:

        try:
            resp = eval(self.session.get(url=self.baseurl%(keyword, page), headers=self.headers).text[17:-1])

        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
        if resp["status"] == 1:
            code                   = ReturnStatus.SUCCESS
            status                 = "ReturnStatus.SUCCESS"
            songList               = ReturnFunction.songList(Data=resp["data"]["info"], songdir="[\"songname_original\"]", artistsdir="[\'singername\']", iddir="[\"hash\"]")
            songList.buidingSongList()
            re_dict_class          = ReturnFunction.RetDataModuleFunc()
            now_page               = page
            before_page, next_page = page-1, page+1
            totalnum               = songList.count
            re_dict                = re_dict_class.RetDataModSearch(now_page, next_page, before_page, songList, totalnum, code=code, status=status)

            return re_dict

    def hash_search(self, hash):
        
        try:
            resp = eval(self.session.get(url=self.hashurl%(hash), headers=self.headers).text)
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
                music_id = resp["hash"]
                re_dict = re_dict_class.RetDataModSong(resp["play_url"], music_id, resp['song_name'], 
                    resp['author_name'], resp['img'], resp['lyrics'], comment=['暂无评论数据'], tlyric='None', 
                    code=code, status=status)

            except:re_dict["code"]    = ReturnStatus.DATA_ERROR
        return re_dict

    def ReturnSongList(self, specialid, page=1):

        url = "http://m.kugou.com/plist/list/%s?json=true"
        try:
            resp = requests.get(url=url%(specialid), headers=self.headers).json()
        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
            return 0
        else:
            try:
                code = ReturnStatus.SUCCESS
                status = "ReturnStatus.SUCCESS"
                image = resp['info']['list']['imgurl']
                re_dict_class = ReturnFunction.RetDataModuleFunc()
    
                songList = ReturnFunction.songList(Data=resp["list"]["list"]['info'], songdir="[\"filename\"]", artistsdir="[\'filename\'][:item[\'filename\'].find(\"-\")]", iddir="[\"hash\"]", page)
                songList.buidingSongList()
                re_dict  = re_dict_class.RetDataModCdlist(resp['info']['list']['specialname'], resp['info']['list']['nickname'],
                                                          resp['info']['list']['intro'], resp['info']['list']['specialid'], 
                                                         image.replace(r"{size}", "400"), songList, resp['list']['list']['total'], 
                                                         resp['list']['list']['total'], code=code, status=status)
                                                         
            except:
                re_dict['code']   = ReturnStatus.DATA_ERROR
            else:
                re_dict['code']   = ReturnStatus.SUCCESS

        return re_dict

    def TopSongList(self):
        url     = "http://m.kugou.com/plist/index&json=true"

        try:
            resp = requests.get(url=url, headers=self.headers).json()
        except simplejson.errors.JSONDecodeError:
            code   = ReturnStatus.ERROR_SEVER
            status = "ReturnStatus.ERROR_SEVER"
            return 0
        else:
            try:
                code = ReturnStatus.SUCCESS
                status = "ReturnStatus.SUCCESS"


                re_dict_class = ReturnFunction.RetDataModuleFunc()

                ItemList = ReturnFunction.TopSongList(Data=resp["plist"]["list"]['info'], 
                                                    ItemNameDir="[\"specialname\"]", 
                                                    ImageUrlDir="[\'imgurl\'].replace(r\"{size}\", \"400\")", 
                                                    IdDir="[\"specialid\"]", InfoDir="[\"intro\"]")
                ItemList.buidingSongList()
                re_dict = re_dict_class.RetDateModHotItemList(ItemList, ItemList.count, code=200, status='Success')

            except:
                re_dict['code'] = ReturnStatus.DATA_ERROR
            else:
                return re_dict



if __name__ == "__main__":

    test = Kugou()

    test.Search_List("浮夸", 1)

