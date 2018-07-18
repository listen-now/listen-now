#!/usr/bin/env python3
# @File:Neteasymusic.py
# @Date:2018/5/9
# Author:Cat.1    
# 2018/05/20 代码部分重构
# 2018/07/15 重构系统
import sys
sys.path.append('..') # 必须要, 设置project为源程序的包顶

from flask import Flask,request,Response,jsonify
import json, time
import re
from Scrawl.NeteasyMusic import NeteasyMusic as neteasy_scrawl
from Scrawl.XiamiMusic import XiamiMusic as xiami_scrawl
from Scrawl.QQMusic import QQMusic as qq_scrawl
import Config.config
from Sync.NeteasySync import Hot_Song_List as neteasy_Hot_Song_List
from Sync.NeteasySync import Neteasymusic_Sync


"""
引入json网页框架用于开放api接口
引入json库用于解析前端上传的json文件
引入AES外部文件用于加密网易云音乐的POST数据
引入scrawl_Neteasymusic、scrawl_Xiamimusic、scrawl_QQmusic用于各个平台的爬虫
引入config文件用于配置数据库等配置信息
"""

re_dict = {}
app = Flask(__name__)
# 形成flask实例


@app.route('/')
def hello_world():
    """
    用于测试服务器是否正常工作.
    """
    return 'Hello World!  This is ZhuYuefeng\'s test_api.  Thanks your requests.  Cat.1'

def _Return_Error_Post(code, status, detail = "", **kw):
    """
    用于向前端反馈错误信息的函数
    包括code参数 错误码
    status     状态信息
    detail     详细信息
    组装数据包成json格式返回
    """
    return {"code":code, "status":status, "detail":detail, "other":kw}




@app.route('/search', methods = ['POST', 'GET'])
def search_json():
    """
    用于接受各类前端的歌曲名字的api请求
    分为POST/GET请求
    如果是POST则又分为
    三大platform平台不同而调起不同的爬虫脚本
    有关更多错误码信息请查阅SDK文档
    """
    global re_dict
    if request.method == 'POST':
        re_dict = {}
        data    = request.get_data()      # 获得json数据包.
        try:
            dict_data = json.loads(data)        # 解析json数据包.
        except:
            re_dict = _Return_Error_Post(code="405", status="Failed", detail = "post not json_data!")
        try:
            music_title    = dict_data["title"]
            music_platform = dict_data["platform"]
            try:
                music_page = dict_data["page"]
            except:
                music_page = 1
            # 获得请求的歌曲名字和选择的音乐平台
        except:
            re_dict = _Return_Error_Post(code="404", status="Failed", detail = "")
        else:
            if music_page > 10:
                re_dict = _Return_Error_Post(code="403", status="Failed", detail = "Is so many response!")

            else:
                if music_title != '' or music_title != None:
                    if music_platform == "Neteasymusic":
                        neteasymusic_id = neteasy_scrawl.Netmusic()
                        re_dict         = neteasymusic_id.pre_response_neteasymusic(music_title, music_page)
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})                            
                        else:
                            re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")
                    elif music_platform == "Xiamimusic":
                        xiamimusic_search = xiami_scrawl.Search_xiami()
                        re_dict       = xiamimusic_search.search_xiami(music_title, music_page)                        
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})
                        else:
                            re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")
                    elif music_platform == "QQmusic":
                        
                        qqmusic_search = qq_scrawl.QQMusic()
                        re_dict        = qqmusic_search.search_by_keyword(music_title, music_page)                        
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})
                        else:
                            re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")

                    else:
                        re_dict = _Return_Error_Post(code="406", status="Failed", detail = "Not know platform!")

                else:
                    re_dict = _Return_Error_Post(code="404", status="Failed", detail = "")
        finally:
            if re_dict == "":
                re_dict = _Return_Error_Post(code="409", status="Failed", detail = "Unknown Error!")

            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')
            return response

    else:
        re_dict = _Return_Error_Post(code="400", status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
        return response

@app.route('/Random_song_list', methods = ['POST', 'GET'])
def Return_Random_User_Song_List():
    """
    用于向前端返回随机的6个歌单信息
    允许GET、POST任何请求均可
    返回的数据格式为 {"0":""}
    """
    global re_dict
    if int(Config.config.getConfig("open_database", "redis")) == 1:
        return_user_song_list = neteasy_Hot_Song_List.Hot_Song_List()
        re_dict = return_user_song_list.Random_Return_func()
        if re_dict:
            re_dict.update({"code":"200", "status":"Success"})
        else:
            re_dict = _Return_Error_Post(code="409", status="Failed", detail = "Unknown Error!")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
        return response
    else:
        re_dict = _Return_Error_Post(code="408", status="Failed", detail = "数据库未启用")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
        return response

@app.route('/user_song_list', methods = ['POST', 'GET'])
def Return_User_Song_List():
    """返回用户的自己的歌单方法
    
    当用户输入他的用户名之后，我们就可以依据用户名（uid）查找用户的歌单，并整理反馈用户收藏
    、创建的歌单信息，以此同步用户各个音乐平台上的歌单，协助用户方便迁移到listen-now
    
    Decorators:
        app.route
    
    Returns:
        dict -- 返回给前端的是一个json包文件，里面含有用户的所有歌单信息。
    """
    global re_dict

    if re.findall(r"wechat", request.headers.get("User-Agent")): # 如果判断用户请求是来自微信小程序
        try:
            user_id = dict_data["open_id"]
        except:
            re_dict     = _Return_Error_Post(code="404", status="Failed", detail = "")


    else:  # 用户来自其他平台
        try:
            user_id = dict_data["user_id"]
        except:
            _Return_Error_Post(code="500", status="Failed", detail = "用户未注册")
        else:
            pass


    data            = request.get_data()     
    try:
        dict_data   = json.loads(data)      
    except:
        re_dict     = _Return_Error_Post(code="405", status="Failed", detail = "post not json_data!")

    try:
        uid         = dict_data["uid"]
        platform    = dict_data["platform"]
    except:
        re_dict     = _Return_Error_Post(code="404", status="Failed", detail = "")
    else:
        if platform == "Neteasymusic":
            check_func  = Neteasymusic_Sync.Neteasymusic_Sync()
            re_dict     = check_func.Get_User_List(uid, user_id)
        elif platform == "QQmusic":
            check_func = qq_scrawl.QQMusic()
            re_dict    = check_func.Get_User_List(uid, user_id)

        re_dict.update({"code":"202", "status":"Success"})
    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
    response.headers.add('Server','python flask')       
    return response


@app.route('/song_list_requests', methods = ['POST', 'GET'])
def Return_User_Song_List_Detail():
    """
    用于向前端返回某一个歌单的详细信息(
                                包括歌单的名称，
                                歌单id，
                                每首歌曲id，
                                歌曲名称，
                                歌曲演唱者
                                )
    """
    global re_dict
    data = request.get_data()     
    try:
        dict_data = json.loads(data)      
    except:
        re_dict = _Return_Error_Post(code="405", status="Failed", detail = "post not json_data!")

    try:
        song_list_platform = dict_data["platform"]
    except:
        re_dict = _Return_Error_Post(code="404", status="Failed", detail = "")
    else:
        if song_list_platform == "Neteasymusic":
            song_list_url         = dict_data["url"]
            return_user_song_list = neteasy_Hot_Song_List.Hot_Song_List()
            re_dict               = return_user_song_list.Download_SongList(song_list_url)
        elif song_list_platform == "QQmusic":
            song_list_id          = dict_data["id"]
            return_user_song_list = qq_scrawl.QQMusic()
            re_dict               = return_user_song_list.get_cdlist(disstid=song_list_id)
        elif song_list_platform == "Xiamimusic":
            pass            

        if re_dict:
            re_dict.update(_Return_Error_Post(code="201", status="Success", detail="None"))
        else:
            re_dict.update(_Return_Error_Post(code="410", status="Failed", detail="没有更多数据或服务器发生错误"))
    
    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
    response.headers.add('Server','python flask')       
    return response

@app.route('/check_user', methods = ['GET','POST'])
def check_user():
    re_dict = {}
    """
    以GET请求方式请求服务器(参数为user_id), 
    得到用户想要注册的用户名,
    检测用户名是否已经被注册.
    如果是返回元祖第一个值为零则表示系统是查询所账户不存在, 可以注册
    返回1表示账户存在, 返回2表示账户新注册成功注册(均同时返回新的账户user_id)
    flag = 1时表示查询账户是否存在, flag = 0时表示当前账户不存在并且希望注册新账户
    value -> 200 表示账户未被注册
          -> 201 账户已经被他人注册
          -> 202 账户注册成功
    """
    if int(Config.config.getConfig("open_database", "redis")) == 1:
        if request.method == 'GET':
            user_id_dict = dict(request.args)
            email      = user_id_dict["user_id"][0]
            try:
                flag   = user_id_dict["flag"][0]
            except KeyError:
                flag = 1
            check_func = Neteasymusic_Sync.Neteasymusic_Sync()
            value      = check_func.Create_Check_User_id(email, int(flag))
            if int(flag[0]) == 1 and value[0] == 0:
                re_dict   = _Return_Error_Post("200", "success", "账户未被注册", value="200")
            elif value[0] == 1:
                re_dict   = _Return_Error_Post("200", "success", "账户已经被他人注册", value="201", user_id=value[1], email=value[2])
            response      = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')       
            return response

        if request.method == 'POST':
            data      = request.get_data()
            dict_data = json.loads(data)   
            flag      = dict_data["flag"]
            email     = dict_data["email"]
            passwd    = dict_data["passwd"]
            # 未完成, 还需要加密过程算法, 存储用户数据到mongodb中
            check_func = Neteasymusic_Sync.Neteasymusic_Sync()
            value      = check_func.Create_Check_User_id(email, int(flag))

            if int(flag[0]) == 0:
                re_dict   = _Return_Error_Post("200", "success", "账户注册成功", value="202", user_id=value[1], email=value[2])

    else:
        re_dict = _Return_Error_Post(code="408", status="Failed", detail = "数据库未启用")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
        return response



@app.route('/id', methods = ['POST', 'GET'])
def play_id():
    """
    用于前端请求歌曲id时服务器针对性的反馈方法
    基本内容如上.
    """
    global re_dict
    if request.method == 'POST':
        data      = request.get_data()
        dict_data = json.loads(data)   
        try:
            music_platform = dict_data['platform']
        except:
            re_dict = _Return_Error_Post(code="404", status="Failed", detail = "")
        else:
            if music_platform != '' or music_platform != None:
                if music_platform == "Neteasymusic":
                    
                    neteasymusic_id = neteasy_scrawl.Netmusic()
                    music_id        = dict_data["id"]
                    re_dict         = neteasymusic_id.music_id_requests(music_id)
                    if re_dict:
                        re_dict.update({"code":"200", "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code="401", status="Failed", detail = "platform not this music!")
                elif music_platform == "Xiamimusic":
                    try:
                        music_id = dict_data["id"]
                    except KeyError:
                        re_dict = _Return_Error_Post(code="404", status="Failed", detail = "")
                    else:
                        re_dict  = xiami_scrawl.Search_xiami.id_req(music_id)
                        print(re_dict)
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")

                elif music_platform == "QQmusic":
                    qqmusic_id = qq_scrawl.QQMusic()
                    re_dict = qqmusic_id.search_by_id(dict_data["id"])

                    if re_dict:
                        re_dict.update({"code":"200", "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")
                else:
                    re_dict = _Return_Error_Post(code="406", status="Failed", detail = "Not know platform!")
        finally:
                response = Response(json.dumps(re_dict), mimetype = 'application/json')    
                response.headers.add('Server','python flask')       
                return response

    else:
        re_dict = _Return_Error_Post(code="400", status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
        return response




if __name__ == '__main__':
    """
    利用configparser库实现读取配置文件的功能
    这里是启用flask的debug模式
    """
    host = Config.config.getConfig("apptest", "apphost")
    port = Config.config.getConfig("apptest", "appport")
    app.run(host=host, port=int(port), debug = True)
    # test
