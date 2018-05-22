#!usr/bin/env python3
# @File:Scrawl_QQmusic.py
# @Date:2018/5/10
# Author:Cat.1

import requests, json

class Qqmusic(object):
    """
    QQ音乐目前只返回前二十个搜索结果.
    由于腾讯官方API限制.
    """
    def __init__(self):
        self.QQmusic_headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Referer':'https://y.qq.com/',
            'Content-Type':'application/x-www-form-urlencoded'
        }
        self.requ_date, self.music_data  = [{} for i in range(2)]


    def qq_music_search(self, title, page = 1):
        url             = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?&lossless=0&flag_qc=0&p=1&n=20&w=%s"
        resp_text       = json.loads(requests.get(url = url %(title), headers = self.QQmusic_headers).text[9:-1])
        self.resp_text    = resp_text
        try: c            = resp_text["data"]['song']["list"][0]["media_mid"]
        except: resp_text = resp_text["data"]['song']["list"][1]
        else: resp_text   = resp_text["data"]['song']["list"][0]
        media_mid        = resp_text["media_mid"]
        songmid          = resp_text["songmid"]
        self.access_resp_text(media_mid, songmid)
        # 调起中值请求爬虫获得vkey数据.
        self.singer_name = resp_text["singer"][0]["name"]
        self.song_name   = resp_text["songname"]        
        self.music_data.update({"artists":self.singer_name, "music_name":self.song_name})
        self.requ_date.update({"0":self.music_data})

        page_end   = page * 10
        page_start = page_end - 9
        if page != 1:
            page_start = page_end - 8
        count = 1
        for i in range(page_start, page_end+1):
            music_data  = {}
            try:
                media_mid   = self.resp_text["data"]['song']["list"][i]["media_mid"]
            except KeyError:
                media_mid = ''
            songmid     = self.resp_text["data"]['song']["list"][i]["songmid"]
            singer_name = self.resp_text["data"]['song']["list"][i]["singer"][0]["name"]
            song_name   = self.resp_text["data"]['song']["list"][i]["songname"]
            music_data.update({"artists": singer_name, "music_name": song_name, "media_mid":media_mid, "songmid":songmid })
            self.requ_date.update({str(count) : music_data})
            count       += 1

        return self.requ_date

    def access_resp_text(self, media_mid, songmid):
        url               = "https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?&jsonpCallback=MusicJsonCallback&cid=205361747&songmid=" + media_mid + "&filename=C400" + songmid + ".m4a&guid=6612300644"
        resp_vkey         = requests.get(url = url, headers = self.QQmusic_headers).json()
        resp_vkey_text    = resp_vkey["data"]["items"][0]["vkey"]
        url               = "http://dl.stream.qqmusic.qq.com/C400%s.m4a?vkey=%s&guid=6612300644&uin=0&fromtag=66" %(songmid, resp_vkey_text)
        self.music_data.update({"play_url":url, "media_mid":media_mid, "songmid":songmid})
        self.requ_date.update({"0":self.music_data})
        return self.requ_date



if __name__ == '__main__':
    test = Qqmusic()
    # print(test.qq_music_search("白金迪斯科"))
    print(test.access_resp_text("004fXf6H2qBjbo", "004fXf6H2qBjbo"))
