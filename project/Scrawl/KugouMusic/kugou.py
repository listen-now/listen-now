# # encoding:utf-8
# import io  
# import sys  
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 


from project.Module import ReturnStatus
from project.Module import RetDataModule
import requests
import copy

class Kugou(object):


    def __init__(self):

        self.baseurl = "http://mobilecdn.kugou.com/api/v3/search/song?format=jsonp&keyword=%s&page=%s&pagesize=10&showtype=1&callback=kgJSONP557904816"
        # 用于搜索并且获取hash的api
        self.hashurl = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s"
        self.session = requests.session()
        self.headers = {
                        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/603.1.13 (KHTML, like Gecko) Version/10.1 Safari/603.1.13',
                        'Referer':'http://mobilecdn.kugou.com/'
                        }


    def Search_List(self, keyword, page) -> str:

        re_dict = copy.deepcopy(RetDataModule.mod_search)
        resp = eval((self.session.get(url=self.baseurl%(keyword, page), headers=self.headers).text)[17:-1])
        if resp["status"] == 1:
            re_dict["code"] = ReturnStatus.SUCCESS
            count           = 0
            for item in resp["data"]["info"]:
                count += 1
                singername  = item["singername"]
                songname    = item["songname_original"]
                hashInfo    = item["hash"]
                return_dict = {"music_name":songname, "artists":singername, "id":hashInfo}
                re_dict["song"]["list"].append(return_dict)
            re_dict['song']["totalnum"] = count
            return re_dict

    def hash_search(self, hash):
        
        re_dict = copy.deepcopy(RetDataModule.mod_song)
        resp = eval(self.session.get(url=self.hashurl%(hash), headers=self.headers).text)

        re_dict["music_name"] = resp["data"]["song_name"]
        re_dict["artists"]    = resp["data"]["author_name"]
        re_dict["lyric"]      = resp["data"]["lyrics"]
        re_dict["image_url"]  = resp["data"]["img"]
        re_dict["play_url"]   = resp["data"]["play_url"]        
        re_dict["music_id"]   = resp["data"]["hash"]

        return re_dict

    def HotSongList(self, specialid):

        url                  = "http://m.kugou.com/plist/list/%s?json=true"
        resp                 = requests.get(url=url%(specialid), headers=self.headers).json()
        re_dict              = copy.deepcopy(RetDataModule.mod_cdlist)
        re_dict["dissname"]  = resp['info']['list']['specialname']
        re_dict["nickname"]  = resp['info']['list']['nickname']
        re_dict['image_url'] = resp['info']['list']['imgurl']
        re_dict['info']      = resp['info']['list']['intro']
        count                = 0
        for item in resp["list"]["list"]['info']:
            count += 1
            song_tag    = item['filename']
            singername  = song_tag[:song_tag.find("-")]
            songname    = song_tag[song_tag.find("-")+2:]
            hashInfo    = item["hash"]
            return_dict = {"music_name":songname, "artists":singername, "id":hashInfo}
            re_dict["song"]["list"].append(return_dict)
        re_dict['song']["totalnum"] = count
        re_dict['dissid']           = resp['info']['list']['specialid']

        return re_dict

if __name__ == "__main__":

    test = Kugou()

    test.Search_List("浮夸", 1)

