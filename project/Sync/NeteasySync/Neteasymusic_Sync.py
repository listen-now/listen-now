#!usr/bin/env python3
# @File:Neteasymusic_Sync.py
# @Date:2018/05/23
# Author:Cat.1

from pymongo import MongoClient
import requests
import redis
import random
import string

from project.Sync.NeteasySync import Hot_Song_List
from project.Config import config


class Neteasymusic_Sync(object):
    """
    这个类是用来同步网易云音乐用户的歌单信息类
    使用该类，用户可以方便的给出网易云音乐的用户名，
    系统会检索出他的歌单信息，并更新到数据库中进行储存
    """


    def __init__(self):
        """
        预处理包括连接mongodb数据库(利用config方法)，设置用户代理等信息
        以及self.Sync_NEM_Url 是获得用户歌单的网易API具体地址
        连接的数据表时mydb, 然后选择mydb中的test_set集合
        """
        host         = config.getConfig("database", "dbhost")
        port         = config.getConfig("database", "dbport")
        self.r       = redis.Redis(host=host, port=int(port), decode_responses=True, db = 2)
        
        host         = config.getConfig("mongodb", "mongodbhost")
        port         = config.getConfig("mongodb", "mongodbport")
        self.conn    = MongoClient(str(host), int(port))
        self.db      = self.conn.mydb
        self.my_set  = self.db.test_set
        self.session = requests.session()
        self.headers = {
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13;rv:57.0) Gecko/20100101 Firefox/57.0',
                        'Referer':"http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=%s"
                        }
        self.Sync_NEM_Url = "http://music.163.com/api/user/playlist/?offset=0&limit=100&uid=%s"

    def Get_User_List(self, uid, user_id=''):
        """
        这个类用于根据用户的uid(网易提供的用户唯一标识来寻找用户)
        根据uid得到用户的歌单信息， 解析返回的json文件，
        整理后依据用户在我们自己平台上的user_id(可由你自定义),
        存入mongodb数据库，后期就依据这个远端同步用户的歌单信息
        但是我们并不详细储存用户歌单数据，针对一个歌单，mongodb中只储存用户的
                            歌单id，歌单封面，歌单名称
        当用户调取时，通过调用Hot_Song_List.py中的Download_SongList办法来
        获得歌单中的详细信息
        用 用户的user_id来检测用户是否是已经同步过歌单, 如果是的话, 则删除其原本歌单.
        再次更新他的新歌单.
        """
        resp    = self.session.get(url = self.Sync_NEM_Url %uid, headers = self.headers)
        content = resp.json()
        Playlist_Num = len(content["playlist"])
        if user_id != '':
            if list(self.my_set.find({"user_id":user_id})) != []:
                self.my_set.remove({'user_id':user_id})
                print("update!")                
            for i in range(Playlist_Num - 1):
                Playlist_name  = content["playlist"][i]["name"]
                Playlist_image = content["playlist"][i]["coverImgUrl"]
                Playlist_id    = content["playlist"][i]["id"]  
                Vi_Num = len(list(self.my_set.find({"user_id":user_id})))
                self.my_set.insert({"user_id":user_id, "Playlist_name":Playlist_name, "Playlist_image":Playlist_image, "Playlist_id":Playlist_id})
        self.requ_date = {}                
        music_data     = {}
        for i in range(Playlist_Num - 1):
            Playlist_name  = content["playlist"][i]["name"]
            Playlist_image = content["playlist"][i]["coverImgUrl"]
            Playlist_id    = content["playlist"][i]["id"]  
            music_data.update({"Playlist_id": Playlist_id, "Playlist_name":Playlist_name, "Playlist_image":Playlist_image})
            try:
                self.requ_date[str(i)].update(music_data)
            except KeyError:
                self.requ_date[str(i)] = {}
                self.requ_date[str(i)].update(music_data)
        self.requ_date['Sum_Song_List'] = i
        return self.requ_date
    
    @staticmethod
    def Get_User_SongList_Detail(url) -> dict:
        """
        通过调用Hot_Song_List类中的静态办法Download_SongList来拿到关于这个歌单的
        具体内容, 并返回一个完整的字典.
        """
        return Neteasymusic_song_maintain_db.Hot_Song_List.Hot_Song_List.Download_SongList(url)
    

    def Create_Check_User_id(self, Sign_in_tags, flag = 1):
        """
        由于使用用户注册信息(他的昵称/邮箱)来作为他的user_id太过不可靠, 
        所以不如直接用他的登录信息来生成一个user_id,
        来储存在redis-2中.
        用redis的dbsize方法来获得目前注册人数, 新注册人的user_id基础信息就是在这个基础上
        加一然后转化为16进制再加上随机产生的8位盐值
        flag = 1 时表示该方法用于查询用户名是否存在, 否则用于创建用户名
        如果用户名存在返回(1,该用户名, 用户想注册账户名), 如果用户新创建账户返回(2, 新user_id, 用户注册的账户名)
        否则用户查询得到没有被注册则返回(0, 0, 用户想注册的账户名)
        """
        user_id = self.r.get(Sign_in_tags)
        if user_id:
            return (1, user_id, Sign_in_tags)
        elif user_id == None and flag != 1:
            cur_value = self.r.dbsize()
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            new_value = hex(cur_value) + salt
            self.r.set(Sign_in_tags, new_value)
            return (2, new_value, Sign_in_tags)
        else:
            return (0, 0, Sign_in_tags)



if __name__ == "__main__":
    
    test = Neteasymusic_Sync()
    test.Get_User_List(252937215)

    # print(Neteasymusic_Sync.Get_User_SongList_Detail("328226111"))
    # print(test.Create_Check_User_id("106995477@q.com", 1))
