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
<<<<<<< HEAD
# print(app1.get_user_profile_dissidlist("1069954477"))
# print(app1.get_cdlist(disstid = "3531843793"))
# print(app1.get_hot_playlist('71'))
# print(app1.get_hot_itemidlist())


from project.Scrawl.NeteasyMusic import NeteasyMusic
app2 = NeteasyMusic.Netmusic()
# print(app2.pre_response_neteasymusic('浮夸'))
print(app2.music_id_requests(66282))
# print(app2.requests_comment("413812448"))


# from project.Scrawl.XiamiMusic.XiamiMusic import Search_xiami
# app3 = Search_xiami()
# print(app3.search_xiami('纸短情长'))


# from project.Helper import bcrypt_hash
# # 登录/注册模块的测试，现已可用
# app4 = bcrypt_hash.loginer()
# print(app4.Sign_Up_Encrypt("The powder toy", "passwd"))
# print(app4.Sign_In_Check("The powder toy", "passwd"))


=======

# from project.Scrawl.NeteasyMusic import NeteasyMusic
# app2 = NeteasyMusic.Netmusic()
# print(app2.pre_response_neteasymusic('大鱼'))

# from project.Scrawl.XiamiMusic.XiamiMusic import Search_xiami
# app3 = Search_xiami()
# print(app3.search_xiami('纸短情长'))


from project.Sync.XiamiSync import XiamiMusic
app4 = XiamiMusic.XiamiApi()
print(app4.getPlaylist("358024020"))
>>>>>>> MscDev
