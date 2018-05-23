#!usr/bin/env python3
# @File:Neteasymusic_Sync.py
# @Date:2018/05/23
# Author:Cat.1

from pymongo import MongoClient
import requests

class Sync_Neteasymusic(object):
    """
    This is a base sarwl , include class, and use requests.session 
    and requests.get/post
    """
    def __init__(self):

        self.conn = MongoClient('127.0.0.1', 27017)
        self.db = self.conn.mydb 
        self.my_set = self.db.test_set

        self.session = requests.session()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13;rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer':"http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=%s"
        }
        self.Sync_NEM_Url = "http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=%s"

    def Get_User_List(self, uid, user_id):
        resp    = self.session.get(url = self.Sync_NEM_Url %uid, headers = self.headers)
        content = resp.json()
        Playlist_Num = len(content["playlist"])
        for i in range(Playlist_Num - 1):
            Playlist_name  = content["playlist"][i]["name"]
            Playlist_image = content["playlist"][i]["coverImgUrl"]
            Playlist_id    = content["playlist"][i]["id"]  
            Vi_Num = len(list(self.my_set.find({"user_id":user_id})))
            self.my_set.insert({"user_id":user_id, "Playlist_name":Playlist_name, "Playlist_image":Playlist_image, "Playlist_id":Playlist_id})
        for i in self.my_set.find({"user_id":"000001"}):
            print(i)
        self.my_set.remove({'user_id': '000001'})                    

if __name__ == "__main__":
    
    test = Sync_Neteasymusic()
    test.Get_User_List(252937215, "000001")