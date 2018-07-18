import sys
sys.path.append('..') #必须要, 设置project为源程序的包顶
# encoding:utf-8
import io  
import sys  
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 


'''
功能测试脚本
'''

from project.Scrawl.QQMusic import QQMusic
app1 = QQMusic.QQMusic()
# print(app1.search_by_keyword('纸短情长'))
# print(app1.get_user_profile_dissidlist("1069954477"))
print(app1.get_cdlist(disstid = "3531843793"))
# print(app1.get_hot_playlist('71'))
# print(app1.get_hot_itemidlist())


# from project.Scrawl.NeteasyMusic import NeteasyMusic
# app2 = NeteasyMusic.Netmusic()
# print(app2.pre_response_neteasymusic('大鱼'))
# print(app2.music_id_requests(444706287))


# from project.Scrawl.XiamiMusic.XiamiMusic import Search_xiami
# app3 = Search_xiami()
# print(app3.search_xiami('纸短情长'))
