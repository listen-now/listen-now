#!/usr/bin/env python3
# @File:Neteasymusic.py
# @Date:2018/5/9
# Author:Cat.1    
# 2018/05/20 代码部分重构
# 2018/07/15 重构系统
# 2018/07/29 增加酷狗音乐支持
# 2018/08/03 Add KuwoMuisc
import sys
sys.path.append('..') # 必须要, 设置project为源程序的包顶
import copy
from flask import Flask,request,Response,jsonify
import json, time
import re
from Scrawl.NeteasyMusic import NeteasyMusic as neteasy_scrawl
from Scrawl.KugouMusic import kugou as kugou_scrawl
from Scrawl.XiamiMusic import XiamiMusic as xiami_scrawl
from Scrawl.QQMusic import QQMusic as qq_scrawl
from Scrawl.KuwoMusic import KuwoMusic as kuwo_scrawl
import Config.config
from Sync.NeteasySync import Hot_Song_List as neteasy_Hot_Song_List
from Sync.NeteasySync import Neteasymusic_Sync
from project.Module import ReturnStatus
from project.Module import RetDataModule
from project.Helper import bcrypt_hash
from Sync.XiamiSync import XiamiMusic as xiami_Song_List
import datetime
import redis
from flask_cors import CORS


"""
引入json网页框架用于开放api接口
引入json库用于解析前端上传的json文件
引入AES外部文件用于加密网易云音乐的POST数据
引入scrawl_Neteasymusic、scrawl_Xiamimusic、scrawl_QQmusic用于各个平台的爬虫
引入config文件用于配置数据库等配置信息
"""

re_dict = {}
if int(Config.config.getConfig("open_database", "redis")) == 1:
    host   = Config.config.getConfig("database", "dbhost")
    port   = Config.config.getConfig("database", "dbport")
    _redis = redis.Redis(host=host, port=int(port), decode_responses=True, db=6)  


app = Flask(__name__)
# 形成flask实例
CORS(app, resources=r'/*')
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求




@app.route('/')
def hello_world():
    """
    用于测试服务器是否正常工作.
    """
    UA = request.headers['User-Agent']
    return UA + 'Hello World!  Listen-now\'s API Working  Cat.1'
    # return 'Hello World!  Listen-now\'s API Working  Cat.1'

def _Return_Error_Post(code, status, detail = "", **kw):
    """
    用于向前端反馈错误信息的函数
    包括code参数 错误码
    status     状态信息
    detail     详细信息
    组装数据包成json格式返回
    """
    return {"code":code, "status":status, "detail":detail, "other":kw}

def Simple_Check(token):
    # 如果token在redis库中，简单认证则通过。

    if token != "" or token != None:
        if _redis.get(str(token[:-5] + '\n' + token[-3:])) == None:
            return 0
        else:
            return 1
    else:
        return 0


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
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail = "post not json_data!")
        try:
            music_title    = dict_data["title"]
            music_platform = dict_data["platform"]
            try:
                music_page = dict_data["page"]
            except:
                music_page = 1
            # 获得请求的歌曲名字和选择的音乐平台
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
        else:
            if music_page > 10:
                re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "Is so many response!")
            else:
                try:
                    token = request.headers['token']
                    if Simple_Check(token) != 1:
                        raise AssertionError
                except AssertionError:
                    re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail = "remind token")
                    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
                    response.headers.add('Server','python flask')       
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response
                except:
                    re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
                    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
                    response.headers.add('Server','python flask')       
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'                    
                    return response

                if music_title != '' or music_title != None:
                    if music_platform == "Neteasymusic":
                        neteasymusic_id = neteasy_scrawl.Netmusic()
                        re_dict         = neteasymusic_id.pre_response_neteasymusic(music_title, music_page)
                        try:
                            re_dict["code"]
                        except KeyError:
                            if re_dict:
                                re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})                            
                            else:
                                re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")
                        else:
                            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_SEVER, status="Failed", detail = "")

                    elif music_platform == "Xiamimusic":
                        xiamimusic_search = xiami_scrawl.Search_xiami()
                        re_dict       = xiamimusic_search.search_xiami(music_title, music_page)                        
                        if re_dict:
                            re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})
                        else:
                            re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")
                    elif music_platform == "QQmusic":
                        
                        qqmusic_search = qq_scrawl.QQMusic()
                        re_dict        = qqmusic_search.search_by_keyword(music_title, music_page)                        
                        try:
                            re_dict["code"]
                        except KeyError:                        
                            if re_dict:
                                re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})
                            else:
                                re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")
                        else:
                            pass
                    elif music_platform == "Kugoumusic":
                        
                        kugou_search = kugou_scrawl.Kugou()
                        re_dict      = kugou_search.Search_List(music_title, music_page)                        
                        try:
                            re_dict["code"]
                        except KeyError:                        
                            if re_dict:
                                re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})
                            else:
                                re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")
                        else:
                            pass

                    elif music_platform == "Kuwomusic":
                        kuwo_search = kuwo_scrawl.Kuwomusic()
                        re_dict     = kuwo_search.Search_List(music_title, music_page)
                        try:
                            re_dict["code"]
                        except KeyError:                        
                            if re_dict:
                                re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success", "now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})
                            else:
                                re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")
                        else:
                            pass

                        finally:
                            re_dict.update({"now_page":music_page, "next_page":music_page + 1, "before_page":music_page - 1})
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.NO_SUPPORT, status="Failed", detail = "Not know platform!")

                else:
                    re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
        finally:
            if re_dict == "":
                re_dict = _Return_Error_Post(code=ReturnStatus.NOT_SAFE, status="Failed", detail = "Unknown Error!")

            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
            return response

    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_METHOD, status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')     
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'          
        return response

@app.route('/Random_song_list', methods = ['POST'])
def Return_Random_User_Song_List():
    """
    用于向前端返回随机的6个歌单信息
    允许GET、POST任何请求均可
    返回的数据格式为 {"0":""}
    """
    global re_dict
    if request.method == "POST":
        data    = request.get_data()      # 获得json数据包.
        try:
            dict_data = json.loads(data)        # 解析json数据包.
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail = "post not json_data!")
        platform = dict_data["platform"]
        
        try:
            token = request.headers['token']
            if Simple_Check(token) != 1:
                raise AssertionError
        except AssertionError:
            re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail = "remind token")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')                   
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')       
        else:
            if platform == "Neteasymusic":
                if int(Config.config.getConfig("open_database", "redis")) == 1:
                    return_user_song_list = neteasy_Hot_Song_List.Hot_Song_List()
                    re_dict = return_user_song_list.Random_Return_func()
                    if re_dict:
                        re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.NOT_SAFE, status="Failed", detail="Unknown Error!")
                    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
                    response.headers.add('Server','python flask')    
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'                       
                    return response
                else:
                    re_dict = _Return_Error_Post(code=ReturnStatus.DATABASE_OFF, status="Failed", detail="数据库未启用")
                    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
                    response.headers.add('Server','python flask')       
            else:
                # 其他平台热门歌单维护
                pass
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'                
        return response

    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_METHOD, status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'               
        return response

@app.route('/login', methods = ["POST"])
def login():
    """登录/注册函数
    
    用于用户登录/注册的api接口，
    用户登录是用户上传他的账户名，明文密码，若登录成功服务器返回cookies，账户名，状态码
    登录失败返回账户名，状态码，状态码可能标示该用户未注册，请求注册的信息，或者是密码错误的信息
    注册功能则是请求账户名，明文密码，flag参数为0
    Decorators:
        app.route
    """
    global re_dict

    data            = request.get_data()     
    try:
        dict_data   = json.loads(data)      
    except:
        re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="post not json_data!")

    if re.findall(r"wechat", request.headers.get("User-Agent")): # 如果判断用户请求是来自微信小程序
        try:
            user_id = dict_data["open_id"]
            passwd  = "Wechat_Mini_Program"            
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="")

    else: # 请求来自非小程序端
        try:
            user_id = dict_data["user_id"]
            passwd  = dict_data["passwd"]            
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="")
    try:
        flag = dict_data["flag"]
    except:flag = 1 # 填写flag参数不为零或者不填写为登录的意思，而不是注册，注册请填写参数为0
    if flag:
        status = bcrypt_hash.Sign_In_Check(user_id, passwd)
        if status["code"] == ReturnStatus.USER_SUCCESS_SIGN_IN or status["code"] == ReturnStatus.USER_WECHAT_SIGN:
            # 用户登录成功
            re_dict = copy.deepcopy(status)

        elif status["code"] == ReturnStatus.USER_FAILED_SIGN_IN:
            re_dict = copy.deepcopy(status)
        elif status["code"] == ReturnStatus.USER_NOT_SIGN_UP:
            re_dict = copy.deepcopy(status)

    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
    response.headers.add('Server','python flask')
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'           
    return response
    
@app.route('/get_token', methods=['POST', 'GET'])
def get_token():
    global re_dict
    outdate=datetime.datetime.today() + datetime.timedelta(days=2)
    if request.method == "POST":
        data            = request.get_data()     
        try:
            dict_data   = json.loads(data)      
        except:
            re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="post not json_data!")

        user_id     = dict_data["user_id"]
        ua          = request.headers.get('User-Agent')
        ip          = request.remote_addr
        creat_token = bcrypt_hash.AES_Crypt_Cookies()
        Token       = creat_token.Creat_Token(1, user_id, ip, ua)        
        re_dict     = {"token_message":str(Token[0]), "signature":str(Token[1])}
        response    = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')  
        response.set_cookie('token', Token[0], expires=outdate)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        return response
    else:
        ua          = request.headers.get('User-Agent')
        ip          = request.remote_addr
        creat_token = bcrypt_hash.AES_Crypt_Cookies()
        Token       = creat_token.Creat_Token(1, "Listen now user", ip, ua)        
        re_dict     = {"token_message":str(Token[0]), "signature":str(Token[1])}
        response    = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')  
        response.set_cookie('token', Token[0], expires=outdate)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'        
        return response

@app.route('/exist_token', methods=['POST'])
def exist_token():
    global re_dict
    outdate=datetime.datetime.today() + datetime.timedelta(days=2)
    data            = request.get_data()     
    try:
        dict_data   = json.loads(data)      
    except:
        re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="post not json_data!")
    if dict_data["sign_valid"] == 1: # 证明签名有效
        try:
            user_id = dict_data["user_id"]
        except KeyError:
            user_id = "Listen now user"
        if _redis.get(dict_data["token"]) != None and _redis.get(dict_data["token"]) == user_id:
            _redis.set(dict_data["token"], user_id)
            if _redis.expire(dict_data["token"], 3600*48):
                re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_IS_EXIST, status="SUCCESS", detail="")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')  
            response.set_cookie('token', dict_data["token"], expires=outdate)
        else:
            re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail="")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')              
    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_CREAT_FAILED, status="Failed", detail="NOT KNOW ERROR!")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')  
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'        
    return response


@app.route('/user_song_list', methods = ['POST', 'GET'])
def Return_User_Song_List():
    """
    处理用户的同步请求
    需要的参数为用户在本平台上的uid以及同步的音乐平台id
    返回的数据包为被同步的歌单信息，用户uid，状态码等
    """
    global re_dict, user_id
    user_id = None
    data            = request.get_data()     
    try:
        dict_data   = json.loads(data)      
    except:
        re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="post not json_data!")
    
    try:
        token = request.headers['token']
        if Simple_Check(token) != 1:
            raise AssertionError
    except AssertionError:
        re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail = "remind token")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask') 
    except:
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
      
    else:
        if re.findall(r"wechat", request.headers.get("User-Agent")): # 如果判断用户请求是来自微信小程序
            try:
                user_id = dict_data["open_id"]
            except:
                re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="")

        else:  
            try:
                user_id = dict_data["user_id"]
            except:
                re_dict = _Return_Error_Post(code=ReturnStatus.USER_NOT_SIGN_UP, status="Failed", detail="用户未注册")
            else:
                pass
        if user_id != None:
            try:
                uid         = dict_data["uid"]
                platform    = dict_data["platform"]
            except:
                re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="")
            else:
                if platform == "Neteasymusic":
                    check_func  = Neteasymusic_Sync.Neteasymusic_Sync()
                    re_dict     = check_func.Get_User_List(uid, user_id)
                elif platform == "QQmusic":
                    check_func = qq_scrawl.QQMusic()
                    re_dict    = check_func.Get_User_List(uid, user_id)
            if re_dict:
                re_dict.update({"code":"202", "status":"Success"})
            else:
                re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_SEVER, status="Failed", detail="")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')    
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'           
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
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail = "post not json_data!")
    try:
        token = request.headers['token']
        if Simple_Check(token) != 1:
            raise AssertionError
    except AssertionError:
        re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail = "remind token")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
    except:
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       

    else:
        try:
            song_list_platform = dict_data["platform"]
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
        else:
            if song_list_platform == "Neteasymusic":
                song_list_url         = dict_data["url"]
                return_user_song_list = neteasy_Hot_Song_List.Hot_Song_List()
                re_dict               = return_user_song_list.Download_SongList(song_list_url)


            elif song_list_platform == "QQmusic":
                song_list_id          = dict_data["id"]
                return_user_song_list = qq_scrawl.QQMusic()
                re_dict               = return_user_song_list.get_cdlist(disstid=song_list_id)
                re_dict = return_user_song_list.Download_SongList(song_list_url)


            elif song_list_platform == "Xiamimusic":
                song_list_url         = dict_data["url"]
                return_song_list = xiami_Song_List.XiamiApi()
                re_dict = retrun_song_list.getPlaylist(song_list_url)


            elif song_list_platform == "Kugoumusic":
                song_list_id     = dict_data["id"]
                return_song_list = kugou_scrawl.Kugou()
                return_song_list.ReturnSongList(song_list_id)

            elif song_list_platform == "Kuwomusic":
                song_list_id    = dict_data["id"]
                return_song_list = kuwo_scrawl.KuwoMusic()
                return_song_list.ReturnSongList(song_list_id)

            if re_dict:
                re_dict.update(_Return_Error_Post(code=ReturnStatus.SUCCESS, status="Success", detail="None"))
            else:
                re_dict.update(_Return_Error_Post(code=ReturnStatus.ERROR_SEVER, status="Failed", detail="没有更多数据或服务器发生错误"))
        
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')     
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'          
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
    if request.method == "POST":
        data = request.get_data()  

        try:
            dict_data = json.loads(data)      
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail = "POST not json_data!")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')     
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'              
            return response

        if re.findall(r"wechat", request.headers.get("User-Agent")): # 如果判断用户请求是来自微信小程序
            try:
                user_id = dict_data["open_id"]
                passwd  = "Wechat_Mini_Program"
            except:
                re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="")

        else:
            user_id = dict_data["user_id"]
            passwd  = dict_data["passwd"]
        try:
            flag = dict_data["flag"]
        except:flag = 1 # 默认flag为登录的意思，而不是注册
        if flag:
            status = bcrypt_hash.Sign_In_Check(user_id, passwd)
            if status["code"] == ReturnStatus.USER_SUCCESS_SIGN_IN or status["code"] == ReturnStatus.USER_WECHAT_SIGN:
                # 如果用户登录成功则请求同步歌单
                pass
        
    elif request.method == "GET":
        pass
    
    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.DATABASE_OFF, status="Failed", detail = "数据库繁忙或遇到技术障碍")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')     
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'          
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
            token = request.headers['token']
            if Simple_Check(token) != 1:
                raise AssertionError
        except AssertionError:
            re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail = "remind token")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')       
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
            return response
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')    
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'               
            return response
        else:
            try:
                music_platform = dict_data['platform']
            except:
                re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
            else:
                if music_platform != '' or music_platform != None:
                    if music_platform == "Neteasymusic":
                        
                        neteasymusic_id = neteasy_scrawl.Netmusic()
                        music_id        = dict_data["id"]
                        re_dict         = neteasymusic_id.music_id_requests(music_id)
                        if re_dict:
                            re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code=ReturnStatus.NO_MUSIC_DETAIL, status="Failed", detail = "platform not this music!")
                    elif music_platform == "Xiamimusic":
                        try:
                            music_id = dict_data["id"]
                        except KeyError:
                            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "")
                        else:
                            re_dict  = xiami_scrawl.Search_xiami.id_req(music_id)
                            print(re_dict)
                            if re_dict:
                                re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                            else:
                                re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")

                    elif music_platform == "QQmusic":
                        qqmusic_id = qq_scrawl.QQMusic()
                        re_dict = qqmusic_id.search_by_id(dict_data["id"])

                        if re_dict:
                            re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")
                    
                    elif music_platform == "Kugoumusic":
                        kugou = kugou_scrawl.Kugou()
                        re_dict = kugou.hash_search(dict_data["id"])

                    elif music_platform == "Kuwomusic":
                        kuwo = kuwo_scrawl.KuwoMusic()
                        re_dict = kuwo.Search_details(dict_data["id"])

                        if re_dict:
                            re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "")
                    
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.NO_SUPPORT, status="Failed", detail = "Not know platform!")
            finally:
                    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
                    response.headers.add('Server','python flask')       
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                    return response

    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_METHOD, status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')      
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'         
        return response




if __name__ == '__main__':
    """
    利用configparser库实现读取配置文件的功能
    这里是启用flask的debug模式
    """

    host = Config.config.getConfig("apptest", "apphost")
    port = Config.config.getConfig("apptest", "appport")
    app.run(host=host, port=int(port), debug = True)

