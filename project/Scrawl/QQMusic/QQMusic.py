
# __fileName__ : QQMusic.py
# __date__ : 2018/07/03
# __author__ : Yaxuan

from project.Module import ReturnStatus
from project.Module import RetDataModule
from .QQHelper.m4aTomp3 import m4aTomp3
import requests
import random
import json
import copy
import re
import os

class QQMusic(object):
    '''
    QQ音乐类
    '''
    cache_path = os.path.abspath('.') + '/QQCache/'
    meta_path = os.path.abspath('.') + '/QQMeta/'
    def __init__(self):
        '''
        会话初始化
        '''
        self.session = requests.Session()
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/603.1.13 (KHTML, like Gecko) Version/10.1 Safari/603.1.13',
            'Referer':'https://y.qq.com/portal/search.html'
        }

    def search_by_keyword(self, keyword, page = 1, num = 10):
        '''
        通过关键字搜索歌曲
        keyword : 关键字
        page : 当前页数[默认=1]
        num : 返回结果最大数量[默认=10]
        返回值 : 歌曲列表
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_search) #拷贝搜索结果模板
        try:
            _url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&'\
            'new_json=1&remoteplace=txt.yqq.top&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0'\
            '&p={0}&n={1}&w={2}&hostUin=0&format=json&inCharset=utf8&'\
            'outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(page, num, keyword)
            response = self.session.request('GET', _url, headers = self.headers)
            serach_res = response.json()
            if serach_res.get('code', -1) == 0:
                song_list = serach_res.get('data',{}).get('song',{}).get('list',[])
                for music in song_list:
                    tmp_song = copy.deepcopy(RetDataModule.mod_song) #拷贝歌曲模板
                    music_id = music['mid']
                    tmp_song['music_id'] = music_id
                    tmp_song['play_url'] = self.get_play_url(music_id, self.get_music_vkey(music_id))
                    tmp_song['music_name'] = music['name']
                    tmp_song['artists'] = music['singer'][0]['name']
                    tmp_song['image_url'] = self.get_image_url(music_id)
                    tmp_song['lyric'] = self.get_music_lyric(music_id)
                    re_dict['song']['list'].append(copy.deepcopy(tmp_song)) #添加到歌曲列表
                    re_dict['song']['totalnum'] += 1
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict

    def search_by_id(self, songMid):
        '''
        通过id搜索歌曲信息
        songMid : 歌曲识别码
        返回值 : 歌曲信息
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_search) #拷贝搜素结果模板
        try:
            _url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid={0}&'\
            'tpl=yqq_song_detail&format=json&loginUin=0&hostUin=0&inCharset=utf8&outCharset=utf-8&'\
            'notice=0&platform=yqq&needNewCode=0'.format(songMid)
            response = self.session.request('GET', _url, headers = self.headers)
            serach_res = response.json()
            if serach_res.get('code', -1) == 0: 
                info = serach_res.get('data')[0]
                tmp_song = copy.deepcopy(RetDataModule.mod_song) #拷贝歌曲模版
                music_id = info['mid']
                tmp_song['music_id'] = music_id
                tmp_song['music_name'] = info['name']   
                tmp_song['artists'] = info['singer'][0]['name']
                tmp_song['play_url'] = self.get_play_url(music_id, self.get_music_vkey(music_id))
                tmp_song['image_url'] = self.get_image_url(music_id)
                tmp_song['lyric'] = self.get_music_lyric(music_id)
                re_dict['song']['list'].append(tmp_song)
                re_dict['song']['totalnum'] += 1
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict

    def get_image_url(self, songMid):
        '''
        获取专辑图像地址
        songMid : 歌曲识别码
        返回值 : 专辑图像地址        
        '''
        return 'http://y.gtimg.cn/music/photo_new/T002R150x150M000{0}.jpg?'\
        'max_age=2592000'.format(songMid)

    def get_play_url(self, songMid, vkey, guid ='1114870539'):
        '''
        获取歌曲地址
        songMid : 歌曲识别码
        vkey : 歌曲vkey
        guid : 用户guid[默认=1114870539]
        返回值 : 歌曲地址
        '''
        return 'http://dl.stream.qqmusic.qq.com/C400{0}.m4a?'\
        'vkey={1}&guid={2}&uin=0&fromtag=66'.format(songMid, vkey, guid)

    def get_music_vkey(self, songMid, guid = '1114870539'):
        '''
        获取歌曲vkey
        songMid : 歌曲识别码
        guid : 用户guid[默认=1114870539]
        返回值 : 歌曲vkey
        '''
        try:
            _url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'\
            'loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&'\
            'platform=yqq&needNewCode=0&cid=205361747&uin=0&songmid={0}&filename=C400{1}.m4a&'\
            'guid={2}'.format(songMid, songMid, guid)
            response = self.session.request('GET', _url, headers = self.headers)
            retjson = response.json()
            return retjson['data']['items'][0]['vkey']
        except:
            return ''

    def get_music_lyric(self, songMid):
        '''
        获取歌曲歌词
        songMid : 歌曲识别码
        返回值 : 歌词
        '''
        try:
            _url = 'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?nobase64=1&pcachetime={0}&'\
            'songmid={1}&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&'\
            'platform=yqq&needNewCode=0'.format(str(random.random())[2:], songMid)
            response = self.session.request('GET', _url, headers = self.headers)
            regStr = 'MusicJsonCallback\((.*)\)'
            result = re.compile(regStr).match(response.text)
            lyric = json.loads(result.group(1))['lyric']
            return lyric
        except:
            return ''

    def get_user_profile_dissidlist(self, uin):
        '''
        获取用户自己创建的歌单的识别码列表， 第一个为默认列表id，其余为创建的歌单id
        返回值id列表 : [default_id, dissid1, dissid2, ...]
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_dissidlist) #拷贝歌单id列表模板
        try:
            _url = 'https://c.y.qq.com/rsc/fcgi-bin/fcg_get_profile_homepage.fcg?loginUin={0}'\
            '&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&'\
            'cid=205360838&ct=20&userid={1}&reqfrom=1&reqtype=0'.format(uin, uin)
            response = self.session.request('GET', _url, headers = self.headers)
            retjson = response.json()
            if retjson.get('code', -1) == 0:
                re_dict['list'].append(retjson.get('data', {}).get('mymusic', [])[0].get('id', 0))
                re_dict['totaldiss'] += 1
                dissids = retjson.get('data', {}).get('mydiss', {}).get('list', [])
                for i in range(retjson.get('data', {}).get('mydiss', {}).get('num', 0) - 1):
                    diss = dissids[i]
                    dissid = diss['dissid'] if str == type(diss['dissid']) else  str(diss['dissid'])
                    re_dict['list'].append(dissid)
                    re_dict['totaldiss'] += 1
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict          

    def get_user_collect_dissidlist(self, uin):
        '''
        获取用户收藏喜欢的歌单的识别码列表
        返回值id列表 : [dissid1, dissid2, ...]
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_dissidlist) #拷贝歌单id列表模板
        try:
            _url = 'https://c.y.qq.com/fav/fcgi-bin/fcg_get_profile_order_asset.fcg?‘\
            ’loginUin={0}&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&'\
            'notice=0&platform=yqq&needNewCode=0&ct=20&cid=205360956&userid={0}&reqtype=3&sin=0&ein=25'.format(uin,uin)
            response = self.session.request('GET', _url, headers = self.headers)
            retjson = response.json()
            if retjson.get('code', -1) == 0:
                cdlists = retjson.get('data', {}).get('cdlist', [])
                for diss in cdlists:
                    dissid = diss['dissid'] if type(diss['dissid']) == str else str(diss['dissid'])
                    re_dict['list'].append(dissid)
                    re_dict['totaldiss'] += 1
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict
                
    def get_cdlist(self, disstid, uin = '447231743',  song_begin = 0, song_num = 10):
        '''
        通过disstid获取的歌单
        disstid : 歌单id
        uin : 用户识别码[]
        song_begin : 歌曲起始索引[默认=0]
        song_num : 欲获取歌曲的数量[默认=10]
        返回值 : 歌单(mod_cdlist格式)
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_cdlist) #歌单模版
        try:
            _url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?'\
            'type=1&json=1&utf8=1&onlysong=0&disstid={0}&format=json&loginUin={1}&hostUin=0'\
            '&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&song_begin={2}'\
            '&song_num={3}'.format(disstid, uin, song_begin, song_num)
            response = self.session.request('GET', _url, headers = self.headers)
            retjson = response.json()
            if retjson.get('code', -1) == 0:
                cdlist = retjson.get('cdlist',[])[0]
                song_list = cdlist.get('songlist', [])
                re_dict['dissid'] = cdlist.get('disstid', disstid)
                re_dict['dissname'] = cdlist.get('dissname', '')
                re_dict['nickname'] = cdlist.get('nickname', '')
                re_dict['song']['totalnum'] = cdlist.get('total_song_num', 0)
                re_dict['song']['curnum'] = cdlist.get('cur_song_num', 0)
                for music in song_list:
                    tmp_song = copy.deepcopy(RetDataModule.mod_song) #拷贝歌曲模板
                    song_id = music['songmid'] if type(music['songmid']) == str else str(music['songmid'])
                    tmp_song['music_id'] = song_id
                    tmp_song['play_url'] = self.get_play_url(song_id, self.get_music_vkey(song_id))
                    tmp_song['music_name'] = music['songname']
                    tmp_song['artists'] = music['singer'][0]['name']
                    tmp_song['image_url'] = 'http://y.gtimg.cn/music/photo_new/'\
                    'T002R150x150M000{0}.jpg?max_age=2592000'.format(song_id)
                    tmp_song['lyric'] = self.get_music_lyric(song_id)
                    re_dict['song']['list'].append(copy.deepcopy(tmp_song))
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict

    def get_hot_itemidlist(self):
        '''
        获取热门推荐itemid列表
        返回值 : [itemid1, itemid2...]
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_hot_item_list) #拷贝推荐主题列表模板
        try:
            _url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?loginUin=0&hostUin=0&format=json&'\
            'inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&'\
            'data={"comm":{"ct":24},"category":{"method":"get_hot_category","param":{"qq":""},'\
            '"module":"music.web_category_svr"},"recomPlaylist":{"method":"get_hot_recommend",'\
            '"param":{"async":1,"cmd":2},"module":"playlist.HotRecommendServer"},"playlist":'\
            '{"method":"get_playlist_by_category","param":{"id":8,"curPage":1,"size":40,"order":5,'\
            '"titleid":8},"module":"playlist.PlayListPlazaServer"},"new_song":{"module":"QQMusic.MusichallServer",'\
            '"method":"GetNewSong","param":{"type":0}},"new_album":{"module":"music.web_album_library","method":'\
            '"get_album_by_tags","param":{"area":1,"company":-1,"genre":-1,"type":-1,"year":-1,"sort":2,"get_tags":1,'\
            '"sin":0,"num":40,"click_albumid":0}},"toplist":{"module":"music.web_toplist_svr","method":"get_toplist_index",'\
            '"param":{}},"focus":{"module":"QQMusic.MusichallServer","method":"GetFocus","param":{}}}'
            response = self.session.request('GET', _url, headers = self.headers)
            retjson = response.json()
            if retjson.get('code', -1) == 0:
                items = retjson.get('category', {}).get('data', {}).get('category', [])[0].get('items',[])
                for item in items:
                    tmp_item = copy.deepcopy(RetDataModule.mod_hot_item) #拷贝主题歌单id列表模板
                    tmp_item['item_id'] = item['item_id'] if type(item['item_id']) == str else str(item['item_id'])
                    if int(tmp_item['item_id']) < 0 : continue
                    tmp_item['item_name'] = item['item_name']
                    tmp_item['item_desc'] = item['item_desc']
                    re_dict['itemlist'].append(copy.deepcopy(tmp_item)) #添加推荐主题
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict

    def get_hot_playlist(self, itemid):
        '''
        获取热门歌单
        itemid : 推荐主题id
        返回值 : 推荐主题的歌单id列表
        ''' 
        re_dict = copy.deepcopy(RetDataModule.mod_hot_dissid_list) #拷贝歌单id列表模板
        try:
            _url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?loginUin=0&hostUin=0&format=json&inCharset=utf8&'\
            'outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&data={"comm":{"ct":24},"playlist":'\
            '{"method":"get_playlist_by_category","param":{"id":%s,"curPage":1,"size":40,"order":5,"titleid":71},'\
            '"module":"playlist.PlayListPlazaServer"}}'%(itemid)
            response = self.session.request('GET', _url, headers = self.headers)
            retjson = response.json()
            tidlist = retjson.get('playlist', {}).get('data', {}).get('v_playlist', [])
            if retjson.get('code', -1) == 0:
                for tid in tidlist:
                    tmp_id = tid['tid'] if type(tid['tid']) == str else str(tid['tid'])
                    re_dict['idlist'].append(tmp_id) #添加到歌单id列表
                    re_dict['totaldiss'] += 1
                else:
                    re_dict['code'] = ReturnStatus.ERROR_SEVER
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
        return re_dict

    def download_song(self, songMid, path = cache_path, transTomp3 = False, guid = '4096863533'):
        '''
        通过歌曲识别码songMid下载音乐
        songMid : 歌曲识别码
        path : 歌曲保存路径[默认缓存路径]
        transTomp3 : 转换为mp3[默认=False]
        guid : 用户识别码[默认=4096863533]
        返回值 : 状态码
        '''
        try:
            if not os.path.exists(path): os.mkdir(path)
            filename = path if path.endswith('/') else path + '/'
            filename +=  songMid + '.m4a'
            exists_m4a = os.path.exists(filename)
            exists_mp3 = os.path.exists(filename.replace('.m4a', '.mp3'))
            if (transTomp3 and not exists_m4a) or (not transTomp3 and not exists_m4a):
                _url = self.get_play_url(songMid, self.get_music_vkey(songMid))
                print(_url)
                if transTomp3 and not exists_mp3 or not transTomp3 and not exists_m4a:
                    response = self.session.request('GET', _url, headers = self.headers)
                    with open(filename, 'wb') as fl:
                        fl.write(response.content)
                if transTomp3: m4aTomp3(filename, filename.replace('.m4a', '.mp3'), rmsrc = True)
            elif transTomp3 and not exists_mp3:     
                m4aTomp3(filename, filename.replace('.m4a', '.mp3'), rmsrc = True)          
            return ReturnStatus.SUCCESS
        except:
            return ReturnStatus.ERROR_UNKNOWN

if __name__ == '__main__':
    app = QQMusic()
    #qquin = '447231743' #qq登陆即为qq号
    print(app.search_by_keyword('纸短情长'))
    #print(app.search_by_id('0015H75B1NvYzl'))
    #print(app.get_user_profile_dissidlist(qquin))
    #print(app.get_hot_itemidlist())
    #print(app.get_hot_playlist('71'))
    #print(app.get_cdlist('4200584372', uin = qquin, song_begin = 0, song_num = 10))
    #print(app.search_songs('张学友', num = 1))
    #print(app.download_song(app.search_songs('张学友', num = 1)['song']['list'][0]['music_id'], transTomp3 = False))
    

