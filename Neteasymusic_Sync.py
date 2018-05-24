#!usr/bin/env python3
# @File:Neteasymusic_Sync.py
# @Date:2018/05/23
# Author:Cat.1

from pymongo import MongoClient
import requests
import config

class Sync_Neteasymusic(object):
    """
    这个类是用来同步网易云音乐用户的歌单信息类
    使用该类，用户可以方便的给出网易云音乐的用户名，
    系统会检索出他的歌单信息，并更新到数据库中进行储存
    """


    def __init__(self):
        """
        预处理包括连接mongodb数据库(利用config方法)，设置用户代理等信息
        以及self.Sync_NEM_Url 是获得用户歌单的网易API具体地址
        """
        host = config.getConfig("mongodb", "mongodbhost")
        port = config.getConfig("apptest", "mongodbport")
        self.conn = MongoClient(str(host), port)
        self.db = self.conn.mydb
        self.my_set = self.db.test_set
        self.session = requests.session()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13;rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer':"http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=%s"
        }
        self.Sync_NEM_Url = "http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=%s"

    def Get_User_List(self, uid, user_id):
        """
        这个类用于根据用户的uid（网易提供的用户唯一标识来寻找用户）
        根据uid得到用户的歌单信息， 解析返回的json文件，
        整理后依据用户在我们自己平台上的user_id（可由你自定义），
        存入mongodb数据库，后期就依据这个远端同步用户的歌单信息
        但是我们并不详细储存用户歌单数据，针对一个歌单，mongodb中只储存用户的
        歌单id，歌单封面，歌单名称
        当用户调取时，通过调用Hot_Song_List.py中的Download_SongList办法来
        获得歌单中的详细信息
        """
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