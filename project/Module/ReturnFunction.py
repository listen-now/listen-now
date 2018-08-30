import copy
from project.Library import Error
from project.Module import ReturnStatus
from project.Module import RetDataModule


class songList(object):
    
    def __init__(self):
        


class RetDateModuleFunc(object):

    def __init__(self):
        self.re_dict = None

    def RetDateModSearch(self, now_page: int, next_page: int, before_page: int, songList: list, 
                         totalnum: int, code='200': str, status='Success': str) -> dict:
        """部分返回参数说明
        
        code -> 请求状态码，参阅ReturnStatus, status -> 详细状态，以str方式提供, now_page -> 当前用户请求的页数为？，用于翻页, 
        songList -> 一种特定的list，主要用来返回规定的歌曲候选列表, totalnum -> 返回的总歌曲数量
        """

        self.re_dict                 = copy.deepcopy(RetDataModule.mod_search)
        self.re_dict['code']         = code
        self.re_dict['status']       = status
        self.re_dict['now_page']     = now_page
        self.re_dict['next_page']    = next_page
        self.re_dict['before_page']  = before_page
        self.re_dict['song']['list'] = songList
        self.re_dict['totalnum']     = totalnum

        return self.re_dict

    def RetDateModSong(self, play_url: str, music_id: str, music_name: str, artists: str, image_url: str, 
                       lyric: str, comment: list, tlyric='NULL': str,  code='200': str, status='Success': str) -> dict:
        """部分返回参数说明
        
        code -> 请求状态码，参阅ReturnStatus, status -> 详细状态，以str方式提供, 
        play_url -> 音乐地址, music_id -> 音乐唯一识别码, lyric -> 歌词信息, tlyric -> 翻译歌词信息
        """

        self.re_dict              = copy.deepcopy(RetDataModule.mod_song)
        self.re_dict['code']      = code
        self.re_dict['status']    = status
        self.re_dict['play_url']  = play_url
        self.re_dict['music_id']  = music_id
        self.re_dict['lyric']     = lyric
        self.re_dict['tlyric']    = tlyric
        self.re_dict['artists']   = artists
        self.re_dict['image_url'] = image_url
        self.re_dict['comment']   = comment

        return self.re_dict



