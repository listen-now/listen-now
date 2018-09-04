# __fileName__ : BaiduMusic.py
# __date__ : 2018/08/01
# __author__ : Yaxuan

from project.Module import ReturnStatus
from project.Module import RetDataModule
from .BaiduHelper.m4aTomp3 import m4aTomp3
import requests
import time
import json
import copy
import re
import os



class BaiduMusic(object):
    '''
    百度音乐
    '''
    cache_path = os.path.abspath('.') + '/Scrawl/BaiduMusic/BaiduCache/'
    meta_path = os.path.abspath('.') + '/Scrawl/BaiduMusic/BaiduMeta/'
    def __init__(self):
        '''
        会话初始化
        '''
        self.session = requests.Session()
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Linux; Android 7.0; SM-G935P Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.92 Mobile Safari/537.36',
            'Referer' : 'http://music.taihe.com/'
        }



    def search_by_keyword(self, keyword, page_no = 1, page_num = 10):
        '''
        通过关键字搜索歌曲
        keyword : 关键字
        page_no : 搜索页[默认 = 1]
        page_num : 搜索页返回歌曲数量[默认 = 10]
        返回值 : 搜索歌曲列表
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_search) #拷贝搜索结果模板
        try:
            _url = 'http://musicapi.taihe.com/v1/restserver/ting?from=webapp_music&format=json&method=baidu.ting.search.merge&'\
            'query={}&page_size={}&page_no={}&type=0,1,2,5,7'.format(keyword, page_num, 0 if page_no == 1 else page_no)
            response = self.session.request('GET', _url, headers = self.headers)
            search_res = response.json()
            if search_res.get('error_code', -1) == 22000:
                song_list = search_res.get('result', {}).get('song_info', {}).get('song_list', [])
                re_dict['song']['totalnum'] = search_res.get('song_info', {}).get('total', 0)
                count = 0
                for song in song_list:
                    tmp_song = copy.deepcopy(RetDataModule.mod_search_song) #拷贝歌曲模板
                    song_id = song['song_id']
                    tmp_song['id'] = song_id
                    tmp_song['music_name'] = song['title']
                    tmp_song['artists'] = song['author']
                    re_dict['song']['list'].append(copy.deepcopy(tmp_song)) #添加到歌曲列表
                    count += 1
                re_dict['song']['totalnum'] = count
            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
                re_dict['status'] = 'ERROR_SEVER'
        except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
        return re_dict



    def search_by_id(self, song_id):
        '''
        通过id搜索歌曲
        song_id : 歌曲id
        返回值 : 歌曲信息
        '''
        re_dict = copy.deepcopy(RetDataModule.mod_song) #拷贝搜素结果模板
        try:
            _url = 'http://musicapi.taihe.com/v1/restserver/ting?from=webapp_music&format=json&'\
            'method=baidu.ting.song.playAAC&songid={}'.format(song_id)
            response = self.session.request('GET', _url, headers = self.headers)
            search_res = response.json()

            if search_res.get('error_code', -1) == 22000:
                info = search_res.get('songinfo', {})
                re_dict['music_id'] = song_id
                re_dict['music_name'] = info['title']   
                re_dict['comment'] = ['暂无评论数据']
                re_dict['artists'] = info['author']
                re_dict['play_url'] = search_res.get('bitrate', {})['file_link']
                re_dict['image_url'] = info['pic_small']
                re_dict['lyric'] = self.get_lyric(info['lrclink'])

            else:
                re_dict['code'] = ReturnStatus.ERROR_SEVER
                re_dict['status'] = 'ERROR_SEVER'
        except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
        return re_dict



    def get_play_url(self, song_id):
        '''
        获取歌曲地址
        song_id : 歌曲识别码
        返回值 : 歌曲地址
        '''
        print(self.cache_path)
        try:
            _url = 'http://musicapi.taihe.com/v1/restserver/ting?from=webapp_music&format=json&'\
            'method=baidu.ting.song.playAAC&songid={}'.format(song_id)
            response = self.session.request('GET', _url, headers = self.headers)
            return response.json().get('bitrate', {})['file_link']
        except Exception:
            return ''



    def get_lyric(self, url):
        '''
        获取歌词
        url : 歌词地址
        返回值 : 歌词
        '''
        try:
            response = self.session.request('GET', url, headers = self.headers)
            return response.text
        except Exception:
            return ''



    def get_user_dissidlist(self):
        '''
        获取用户歌单id列表
        '''
        pass



    def get_hot_itemidlist(self):
        '''
        获取热门推荐itemid列表
        '''
        pass



    def get_hot_playlist(self):
        '''
        获取热门推荐歌单id列表
        '''
        pass



    def get_cdlist(self, listid):
        '''
        获取歌单列表
        listid : 歌单id
        '''
        _param = 'ytploR2aoTXKZYJtPHEu+S171e1Kd7H9oOJx5R96zumtyz3rnBVG17o06TlY0f+P9nJD8Sga4CzSx/nXo/2Ybw=='
        _sign = '22fe3bd57c73bc5903d66076c64f7559'
        _timestamp = 1533254462

        _url = 'http://musicapi.taihe.com/v1/restserver/ting?from=webapp_music&format=json&'\
        'param={}&timestamp={}&sign={}&method=baidu.ting.ugcdiy.getBaseInfo'.format(_param, _timestamp, _sign)
        response = self.session.request('GET', _url, headers = self.headers)
        print(response.json())



    def get_ranndom_playlist(self, num = 6):
        '''
        获取随机歌单
        num : 歌单数量[默认=6]
        '''
        pass



    def download_song(self, song_id, path = cache_path, transTomp3 = False):
        '''
        通过歌曲识别码song_id下载音乐
        song_id : 歌曲识别码
        path : 歌曲保存路径[默认缓存路径]
        transTomp3 : 转换为mp3[默认=False]
        guid : 用户识别码[默认=4096863533]
        返回值 : 状态码
        '''
        try:
            if not os.path.exists(path): os.mkdir(path)
            filename = path if path.endswith('/') else path + '/'
            filename +=  song_id + '.m4a'
            exists_m4a = os.path.exists(filename)
            exists_mp3 = os.path.exists(filename.replace('.m4a', '.mp3'))
            if (transTomp3 and not exists_m4a) or (not transTomp3 and not exists_m4a):
                _url = self.get_play_url(song_id)
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
    app = BaiduMusic()
    #app.search_by_keyword('张学友')
    #app.search_by_id(312707)
