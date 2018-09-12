import sys
sys.path.append('..') #必须要, 设置project为源程序的包顶
# encoding:utf-8
import io  
import sys  
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 


'''
功能测试脚本
'''

# from project.Scrawl.QQMusic import QQMusic
# app1 = QQMusic.QQMusic()
# print(app1.search_by_keyword('纸短情长'))
# print(app1.search_by_id("0026dJ8k47cwSU"))
# print(app1.get_cdlist(3644190836, page=2))

# from project.Scrawl.BaiduMusic import BaiduMusic
# app = BaiduMusic.BaiduMusic()
# print(app.search_by_keyword('张学友'))

# from project.Scrawl.XiamiMusic.XiamiMusic import Search_xiami
# app3 = Search_xiami()
# print(app3.search_xiami('纸短情长'))
# from project.Sync.XiamiSync import XiamiMusic
# app4 = XiamiMusic.XiamiApi()
# print(app4.getPlaylist("358024020"))


# print(app1.get_user_profile_dissidlist("1069954477"))
# print(app1.get_cdlist(disstid = "3531843793"))
# print(app1.get_hot_playlist('71'))
# print(app1.get_hot_itemidlist())


# from project.Scrawl.NeteasyMusic import NeteasyMusic
# app2 = NeteasyMusic.Netmusic()
# # print(app2.pre_response_neteasymusic('浮夸'))
# print(app2.music_id_requests(471411438))
# print(app2.requests_comment("413812448"))



# from project.Sync.NeteasySync import Hot_Song_List
# test = Hot_Song_List.Hot_Song_List()
# test.Download_SongList("2196054076")

#from project.Helper import bcrypt_hash
#app4 = bcrypt_hash.loginer()
#app5 = bcrypt_hash.AES_Crypt_Cookies()
# print(app4.Sign_Up_Encrypt("The powder toy", "passwd"))
# print(app4.Sign_In_Check("The powder toy", "passwd"))
# print(app5.Creat_Token(1, "Listen now user", "115.238.228.39", "Wechat Firefox"))
# print(app5.Decrypt_Check_Token(b'\xd7\x93x\xc1\xe2~@\xd1\x88\xc4\x15\xb5a\xbb,\x1a\xe7599\xa2\xbc\xa5\x05"\xf4R\xa1\x80\x04\xa6\x8a\x82\xb0\xb2^\xb5\xae\xa2N\xb8\xcf\xba`\'9\xd7C\xf7\xf3\x1cu\xf3\xe8\x8akU\\\r\xcb\x90\xd1i\xa2\x99\xad\x15"\xe3\xb4\xe8\x9f\xb3\xa5\xc6\x03x\xf4\x1aI', "115.238.228.39", "Wechat Firefox"))
# app4.Check_Token(b'c+D+2FdJbUXSY9QLB1UvH8P0/EbqBSz5Km+XRTFiAmCsh19V7nOdxzbVRlc7c2tIwSTgiHBx9tDacxqq49wcrkXApsH232oD7XKbuyHzFVk=\nNQZ',
# "115.238.228.39", 
# "Wechat Firefox")


from project.Scrawl.KuwoMusic import KuwoMusic
app7 = KuwoMusic.KuwoMusic()
# print(app7.Search_List("青花瓷", 1))
#print(app7.Search_details("50601684"))
# print(app7.get_play_url("48791034"))
# print(app7.get_comment("48791034"))
print(app7.get_songlist('88152'))


# from project.Scrawl.MiguMusic import MiguMusic
# app8 = MiguMusic.Migu()
# print(app8.search("怪咖", 1))
# print(app8.search_details('60075020337'))


# from project.Scrawl.KugouMusic import kugou
# app7 = kugou.Kugou()
# # print(app7.Search_List("纸短情长", 1))
# # print(app7.hash_search("c592091f71226cd2dc9f840655b235bb"))
# print(app7.ReturnSongList("521431"))
# # print(app7.TopSongList())



# from Helper.token_admin import Forbidden

# app8 = Forbidden()
# print(app8.sign_ip("1234test"))


# from project.Sync.XiamiSync import XiamiMusic
# app9 = XiamiMusic.XiamiApi()
# print(app9.getPlaylist('358024020'))