# __fileName__ : RetDataModule.py
# __date__ : 2018/07/08
# __author__ : Yaxuan

mod_search = {
    'code' : '200',
    'status' : 'Success',
    'now_page' : 1,
    'next_page' : 2,
    'before_page' : 0,
    'song': {
        'totalnum' : 0,
        'list' : []
    }
} #搜索结果json模板

mod_dissidlist = {
    'code' : '200',
    'status' : 'Success',
    'totaldiss' : 0,
    'list' : [],
    'comment':[],
} #歌单id列表json模板

mod_cdlist = {
    'dissid' : '',
    'dissname' : '我喜欢',
    'nickname' : '默认列表',
    'song' : {
        'totalnum' : 0,
        'curnum' : 0,
        'list' : []
    }
} #歌单json模板

mod_song = {
    'play_url' : '',
    'music_id' : '',
    'music_name' : '',
    'artists' : '',
    'image_url' : '',
    'lyric' : ''
} #歌曲json模板

mod_hot_item_list = {
    'code' : '200',
    'status' : 'Success',
    'totalitem' : 0,
    'itemlist' : []
} #推荐主题列表json模板

mod_hot_item = {
    'item_id' : '',
    'item_name' : '粤语',
    'item_desc' : '越动越难听',
} #推荐主题json模板

mod_hot_dissid_list = {
    'code' : '200',
    'status' : 'Success',
    'totaldiss' : 0,
    'idlist' : []
} #推荐主题歌单id列表json模板
