# __date__ 2018/7/29
# __file__ KuwoMusic
# __author__ Msc
# encoding:utf-8

import requests
import re
import json
import copy
import simplejson
from project.Module import ReturnStatus
from project.Module import RetDataModule

class KuwoMusic(object):
    '''
        酷我音乐
    '''
    re_dict = copy.deepcopy(RetDataModule.mod_search)
    def __init__(self):
        self.baseurl = "http://search.kuwo.cn/r.s?all=%s&ft=music&itemset=web_2013&client=kt&pn=%s&rn=%s&rformat=\
                json&encoding=utf8"
        self.palyurl = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid=%s&format=aac|mp3&response=url"
        self.imageurl = "http://artistpicserver.kuwo.cn/pic.web?type=big_artist_pic&pictype=url&content=list&&id=0&name=&rid=%s&from=pc&json=1&version=1&width=1366&height=768"
        self.commiturl = "http://comment.kuwo.cn/com.s?type=get_comment&uid=0&prod=newWeb&digest=15&sid=%s&page=1&rows=10&f=web"
        self.session = requests.session
        self.header = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer':base_url
        }

    def Search_List(self,keyword,page,num = 10) -> str:

        re_dict = copy.deepcopy(RetDataModule.mod_search)
        try:
            resp = eval(self.session.get(url=self.baseurl%(keyword,page,num),headers=self.headers).text)
        except simplejson.error.JSONDecodeError:
            re_dict["code"] = ReturnStatus.ERROR_SEVER
            return re_dict
        try:
            for item in resp["abslist"]:
                count += 1
                singer = item["artist"]
                songname = item["songname"]
                music_id = item["musicrid"][6:]
                return_dict = {"music_name":songname,"artist":singer,"id":musicrid}
                re_dict["song"]["list"].append(return_dict)
            re_duct["song"]["totalnum"] = count
            return re_dict

    def Search_details(self,music_id):
        re_dict = copy.deepcopy(RetDataModule.mod_song)

        try:
            re_dict["music_id"] = self.Search_List 
            re_dict["music_name"] = 
            re_dict["artists"] = 
            re_dict["play_url"] = self.get_play_url(music_id)
            re_dict["lyric"] = self.get_lyric(music_id)
            re_dict["image_url"] = self.get_image(music_id)
            re_dict["comment"] = self.get_comment(music_id)
        except:re_dict["code"]    = ReturnStatus.DATA_ERROR
        else:re_dict["code"]      = ReturnStatus.SUCCESS
        return re_dict


    def get_play_url(self,music_id):
        re_dict = copy.deepcopy(RetDataModule.mod_song)

        play_url = "http://antiserver.kuwo.cn/anti.s?type=convert_url&rid={0}&format=aac|mp3&response=url".format(music_id)
        return play_url

    def get_lyric(self,music_id):
        re_dict = copy.deepcopy(RetDataModule.mod_song)


        resp = requests.get(url='http://www.kuwo.cn/yinyue/{0}}?catalog=yueku2016,headers=self.headers'.format(music_id)).text
        head = resp.find('var lrcList')
        end = resp.find('] || []')
        lyric = resp[head+15:end]
        return lyric

    def get_image(self,music_id):
        re_dict = copy.deepcopy(RetDataModule.mod_song)
        resp = eval(self.session.get(url=self.imageurl%(music_id),headers=self.headers).text)
        image = resp["array"]["bkurl"][0]
        return image

    def get_comment(self,music_id):
        resp = eval(self.session.get(url=self.commiturl%(music_id),headers=self.headers).text)
        comment = resp["rows"]
        return comment




if __name__=="__main__":

    test = KuwoMusic()

    rest.Search_List("青花瓷",1,10)











