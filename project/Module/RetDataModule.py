# __fileName__ : RetDataModule.py
# __date__ : 2018/07/08
# __author__ : Yaxuan
# __Update__: Cat.1


mod_search_song = {
    "music_name":"",
    "artists":"",
    "id":""
    }

mod_search = {
    'code' : 200,
    'status' : 'Success',
    'now_page' : 1,
    'next_page' : 2,
    'before_page' : 0,
    'song': {
        'totalnum' : 0,
        'list' : []
    }
} # 搜索结果json模板

mod_dissidlist = {
    'code' : 200,
    'status' : 'Success',
    'totaldiss' : 0,
    'list' : []
} #歌单id列表json模板

mod_cdlist = {
    'code' : 200,
    'status' : 'Success',
    'dissid' : '',
    'dissname' : '我是这个歌单的名字',
    'nickname' : '我是这个歌单的创建者的名字',
    'info':'',
    'image_url':'',
    'song' : {
        'totalnum' : 0,
        'curnum' : 0,
        'list' : []
    }
} #歌单json模板

mod_song = {
    'code' : 200,
    'status' : 'Success',
    'play_url' : '',
    'id' : '',
    'music_name' : '',
    'artists' : '',
    'image_url' : '',
    'lyric' : '',
    'tlyric':'',
    'comment':[]
} # 歌曲json模板

mod_hot_item_list = {
    'code' : 200,
    'status' : 'Success',
    'totalitem' : 0,
    'itemlist' : [
              {
                'item_id' : '',
                'item_name' : '粤语',
                'item_desc' : '越动越好听，经典的粤语合集给你',
                'image_url' : '',
               },
            ]
} # 推荐主题列表json模板


mod_hot_item = {
    'item_id' : '',
    'item_name' : '粤语',
    'item_desc' : '越动越好听，经典的粤语合集给你',
    'image_url' : '',
} # 推荐主题的json模板，包括主题id

mod_hot_dissid_list = {
    'code' : 200,
    'status' : 'Success',
    'item_name' : '粤语',
    'item_desc' : '越动越好听，经典的粤语合集给你',
    'totaldiss' : 0,
    'idlist' : []
} # 推荐主题歌单id列表json模板，针对某一个主题歌单的id综合

mod_sign = {
    'code'   : 200,
    'status' : 'Success',
    'user_id': 0, 
    'token_status': "",
    'token_message':""
} # 注册登录信息模板，新平台上开发用不到

mod_token = {
    'code'   : 200,
    'status' : 'Success',
    'ip':"",
    'token_status': "",
    'other':"",
} # 注册登录信息模板，新平台上开发用不到

