#!/usr/bin/env python3
# @File:main.py
# @Date:2018/5/9
# Author:Cat.1    
# 2018/05/20 代码部分重构
# 2018/07/15 重构系统
# 2018/07/29 增加酷狗音乐初步支持
# 2018/08/03 增加百度、酷我音乐初步支持
# 2018/08/25 增加Spotify初步支持

#t
#te
#tes
#test
#testt
#testte
#testtes
import re
import sys
import copy
import redis
import datetime
import threading
import json, time
sys.path.append('..')
from flask_cors import CORS
import project.Config.config 
from project.Library import Error
from project.Helper import bcrypt_hash
from project.Helper import token_admin 
from project.Module import ReturnStatus
from project.Module import RetDataModule
from flask import render_template,redirect
from flask import Flask,request,Response,jsonify
from project.Sync.NeteasySync import Neteasymusic_Sync
from project.Scrawl.QQMusic import QQMusic as qq_scrawl
from project.Scrawl.KugouMusic import kugou as kugou_scrawl
from project.Scrawl.KuwoMusic import KuwoMusic as kuwo_scrawl
from project.Scrawl.MiguMusic import MiguMusic as migu_scrawl
# from project.Scrawl.SpotifyMusic import SpotifyMusic as spotify
from project.Scrawl.BaiduMusic import BaiduMusic as baidu_scrawl
from project.Sync.XiamiSync import XiamiMusic as xiami_Song_List
from project.Scrawl.XiamiMusic import XiamiMusic as xiami_scrawl
from project.Scrawl.NeteasyMusic import NeteasyMusic as neteasy_scrawl
from project.Sync.NeteasySync import Hot_Song_List as neteasy_Hot_Song_List



"""
引入json网页框架用于开放api接口
引入json库用于解析前端上传的json文件
引入AES外部文件用于加密网易云音乐的POST数据
引入Scrawl用于各个平台的爬虫
引入config文件用于配置数据库等配置信息
引入Sync文件用不各个平台歌单信息同步
引入Module文件用于规定各个平台返回数据的格式和针对不同状况的错误处理码
引入flask_cors用于运行跨域访问
"""


"""
>>>以下为部分全局参数设定>>>

"""

re_dict = {}
if int(project.Config.config.getConfig("open_database", "redis")) == 1:
    host   = project.Config.config.getConfig("database", "dbhost")
    port   = project.Config.config.getConfig("database", "dbport")
    _redis = redis.Redis(host=host, port=int(port), decode_responses=True, db=6)  

# sp = spotify.Spotify(2) # 必要的全局变量 参数是保持的待用驱动数 一个驱动可以处理一个用户

app = Flask(__name__)
# 形成flask实例
CORS(app, resources=r'/*')
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求

re_value_, re_value = 0, 0



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
    global re_value
    if token != "" or token != None:
        print("result = ", _redis.get(str(token[:-5] + '\n' + token[-3:])))
        if _redis.get(str(token[:-5] + '\n' + token[-3:])) == None:
            re_value = 0
            return 0
        else:
            re_value = 1
            return 1
    else:
        re_value = 0
        return 0



def Contorl_Request(token):
    global re_value_

    check = token_admin.Forbidden()
    re_value_ = check.sign_ip(token)
    if re_value_["code"] == ReturnStatus.TOKEN_SUCCESS:
        re_value_ = 1
        return re_value_
    elif re_value_["code"] == ReturnStatus.IP_FORBID:
        re_value_ = 0
        return re_value_



def Test_api(token):
    try:
        t1 = threading.Thread(target=Simple_Check, args=(token,))
        t2 = threading.Thread(target=Contorl_Request, args=(token,))
        # 启动异步线程查询数据
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        if re_value != 1:
            # token 不合法
            raise Error.Token_Time_Error()
        elif re_value == 1 and re_value_ != 1:
            # token 受到频率控制
            raise Error.Token_Contorl_Error()

    except Error.Token_Time_Error:
        return ReturnStatus.TOKEN_ERROR

    except Error.Token_Contorl_Error:
        return ReturnStatus.TOKEN_FORBED
    else:
        return 1




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
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail = "ERROR_PSOT_DATA")
        try:
            music_title    = dict_data["title"]
            music_platform = dict_data["platform"]
            try:
                music_page = dict_data["page"]
            except:
                music_page = 1
            # 获得请求的歌曲名字和选择的音乐平台
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
        else:
            if music_page > 10:
                re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "OVER_MAXPAGE")
            else:
                if music_title != '' or music_title != None:
                    if music_platform == "Neteasemusic":
                        neteasymusic_id = neteasy_scrawl.Netmusic()
                        re_dict         = neteasymusic_id.pre_response_neteasymusic(music_title, music_page)

                    elif music_platform == "Xiamimusic":
                        xiamimusic_search = xiami_scrawl.Search_xiami()
                        re_dict       = xiamimusic_search.search_xiami(music_title, music_page)                        

                    elif music_platform == "QQmusic":                        
                        qqmusic_search = qq_scrawl.QQMusic()
                        re_dict        = qqmusic_search.search_by_keyword(music_title, music_page)                        

                    elif music_platform == "Kugoumusic":
                        
                        kugou_search = kugou_scrawl.Kugou()
                        re_dict      = kugou_search.Search_List(music_title, music_page)                        


                    elif music_platform == "Kuwomusic":
                        kuwo_search = kuwo_scrawl.KuwoMusic()
                        re_dict     = kuwo_search.Search_List(music_title, music_page)


                    elif music_platform == "Migumusic":
                        migu_search = migu_scrawl.Migu()
                        re_dict     = migu_search.search(music_title, music_page)

                    elif music_platform == "Baidumusic":
                        baidu_search = baidu_scrawl.BaiduMusic()
                        re_dict      = baidu_search.search_by_keyword(keyword=music_title, page_no=music_page, page_num=10)

                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.NO_SUPPORT, status="Failed", detail = "NO_SUPPORT")

                else:
                    re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
        finally:
            if re_dict == "":
                re_dict = _Return_Error_Post(code=ReturnStatus.NOT_SAFE, status="Failed", detail = "NOT_SAFE")
            elif re_dict = ReturnStatus.NO_EXISTS:
                re_dict = _Return_Error_Post(code=ReturnStatus.NO_EXISTS, status="Failed", detail = "NO_EXISTS")
                
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
            return response

    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_METHOD, status="Failed", detail = "ERROR_METHOD")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')     
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'          
        return response




@app.route('/TopSongList', methods = ['POST', "GET"])
def Return_Random_User_Song_List():
    """
    用于向前端返回20个热门歌单信息
    允许GET、POST任何请求均可
    """
    global re_dict
    if request.method == "POST":
        pass
        # 暂时重新修改代码
    else:

        KugouTopSongList = kugou_scrawl.Kugou()
        re_dict          = KugouTopSongList.TopSongList()
        print(re_dict)

        response         = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
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
        re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="ERROR_PSOT_DATA")

    if re.findall(r"wechat", request.headers.get("User-Agent")): # 如果判断用户请求是来自微信小程序
        try:
            user_id = dict_data["open_id"]
            passwd  = "Wechat_Mini_Program"            
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="ERROR_PARAMS")

    else: # 请求来自非小程序端
        try:
            user_id = dict_data["user_id"]
            passwd  = dict_data["passwd"]            
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="ERROR_PARAMS")
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
    response.headers['Access-Control-Allow-Origin']   = '*'
    response.headers['Access-Control-Allow-Methods']  = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers']  = 'x-requested-with'           
    return response
    



@app.route('/get_token', methods=['GET'])
def get_token():
    global re_dict
    outdate=datetime.datetime.today()
    if request.method == "POST":
        data            = request.get_data()     
        try:
            dict_data   = json.loads(data)      
        except:
            re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="ERROR_PSOT_DATA")

        user_id     = dict_data["user_id"]
        ua          = request.headers.get('User-Agent')
        ip          = request.remote_addr
        creat_token = bcrypt_hash.AES_Crypt_Cookies()
        Token       = creat_token.Creat_Token(1, user_id, ip, ua)        
        re_dict     = {"token_message":str(Token[0]), "signature":str(Token[1])}
        response    = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')  
        response.set_cookie('token', Token[0], expires=outdate)
        response.headers['Access-Control-Allow-Origin']      = '*'
        response.headers['Access-Control-Allow-Methods']     = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers']     = 'x-requested-with'
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
        response.headers['Access-Control-Allow-Origin']      = '*'
        response.headers['Access-Control-Allow-Methods']     = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers']     = 'x-requested-with'        
        return response




@app.route('/exist_token', methods=['POST'])
def exist_token():
    global re_dict
    outdate=datetime.datetime.today() + datetime.timedelta(days=2)
    data            = request.get_data()     
    try:
        dict_data   = json.loads(data)      
    except:
        re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="ERROR_PSOT_DATA")
    if dict_data["sign_valid"] == 1: # 证明签名有效
        try:
            user_id = dict_data["user_id"]
        except KeyError:
            user_id = "Listen now user"
        if _redis.get(dict_data["token"]) != None and _redis.get(dict_data["token"]) == user_id:
            _redis.set(dict_data["token"], user_id)
            if _redis.expire(dict_data["token"], 3600*48):
                re_dict = _Return_Error_Post(code=ReturnStatus.TOKEN_IS_EXIST, status="SUCCESS", detail="TOKEN_IS_EXIST")
            response    = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')  
            response.set_cookie('token', dict_data["token"], expires=outdate)
        else:
            re_dict  = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail="TOKEN_ERROR")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')              
    else:
        re_dict  = _Return_Error_Post(code=ReturnStatus.TOKEN_CREAT_FAILED, status="Failed", detail="TOKEN_CREAT_FAILED")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')  
    response.headers['Access-Control-Allow-Origin']       = '*'
    response.headers['Access-Control-Allow-Methods']      = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers']      = 'x-requested-with'        
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
        re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail="ERROR_PSOT_DATA")
    
    if re.findall(r"wechat", request.headers.get("User-Agent")): # 如果判断用户请求是来自微信小程序
        try:
            user_id = dict_data["open_id"]
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="ERROR_PARAMS")

    else:  
        try:
            user_id = dict_data["user_id"]
        except:
            re_dict = _Return_Error_Post(code=ReturnStatus.USER_NOT_SIGN_UP, status="Failed", detail="USER_NOT_SIGN_UP")
        else:
            pass
    if user_id != None:
        try:
            uid         = dict_data["uid"]
            platform    = dict_data["platform"]
        except:
            re_dict     = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="ERROR_PARAMS")
        else:
            if platform == "Neteasemusic":
                check_func  = Neteasymusic_Sync.Neteasymusic_Sync()
                re_dict     = check_func.Get_User_List(uid, user_id)
            elif platform == "QQmusic":
                check_func = qq_scrawl.QQMusic()
                re_dict    = check_func.Get_User_List(uid, user_id)
        if re_dict:
            re_dict.update({"code":202, "status":"Success"})
        else:
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_SEVER, status="Failed", detail="ERROR_SEVER")
    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
    response.headers.add('Server','python flask')    
    response.headers['Access-Control-Allow-Origin']   = '*'
    response.headers['Access-Control-Allow-Methods']  = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers']  = 'x-requested-with'           
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
        dict_data          = json.loads(data)      
    except:
        re_dict            = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail = "ERROR_PSOT_DATA")
    try:
        song_list_platform = dict_data["platform"]
    except:
        re_dict            = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
    
    song_list_id           = dict_data["id"]
    page                   = dict_data['page']


    if song_list_platform == "Neteasemusic":
        return_user_song_list = neteasy_Hot_Song_List.Hot_Song_List()
        re_dict               = return_user_song_list.Download_SongList(song_list_id)
    
    elif song_list_platform == "Xiamimusic":
        return_song_list = xiami_Song_List.XiamiApi()
        re_dict          = retrun_song_list.getPlaylist(song_list_id)

    elif song_list_platform == "Kugoumusic":
        return_user_song_list = kugou_scrawl.Kugou()
        re_dict               = return_user_song_list.ReturnSongList(song_list_id, page)
    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.NO_SUPPORT, status="Failed", detail = "NO_SUPPORT")


    if re_dict:
        re_dict.update(_Return_Error_Post(code=ReturnStatus.SUCCESS, status="Success", detail="SUCCESS"))
    else:
        re_dict.update(_Return_Error_Post(code=ReturnStatus.ERROR_SEVER, status="Failed", detail="ERROR_SEVER"))
    
    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
    response.headers.add('Server','python flask')     
    response.headers['Access-Control-Allow-Origin']   = '*'
    response.headers['Access-Control-Allow-Methods']  = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers']  = 'x-requested-with'          
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
            re_dict  = _Return_Error_Post(code=ReturnStatus.ERROR_PSOT_DATA, status="Failed", detail = "ERROR_PSOT_DATA")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')     
            response.headers['Access-Control-Allow-Origin']   = '*'
            response.headers['Access-Control-Allow-Methods']  = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers']  = 'x-requested-with'              
            return response

        if re.findall(r"wechat", request.headers.get("User-Agent")): # 如果判断用户请求是来自微信小程序
            try:
                user_id = dict_data["open_id"]
                passwd  = "Wechat_Mini_Program"
            except:
                re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail="ERROR_PARAMS")

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
        re_dict = _Return_Error_Post(code=ReturnStatus.DATABASE_OFF, status="Failed", detail = "DATABASE_OFF")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')     
        response.headers['Access-Control-Allow-Origin']   = '*'
        response.headers['Access-Control-Allow-Methods']  = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers']  = 'x-requested-with'          
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
            re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
        else:
            if music_platform != '' or music_platform != None:
                if music_platform == "Neteasemusic":
                    
                    neteasymusic_id = neteasy_scrawl.Netmusic()
                    music_id        = dict_data["id"]
                    re_dict         = neteasymusic_id.music_id_requests(music_id)
                    if re_dict:
                        re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.NO_MUSIC_DETAIL, status="Failed", detail = "NO_MUSIC_DETAIL")
                elif music_platform == "Xiamimusic":
                    try:
                        music_id = dict_data["id"]
                    except KeyError:
                        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
                    else:
                        re_dict  = xiami_scrawl.Search_xiami.id_req(music_id)
                        print(re_dict)
                        if re_dict:
                            re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "OVER_MAXPAGE")

                elif music_platform == "QQmusic":
                    qqmusic_id = qq_scrawl.QQMusic()
                    re_dict = qqmusic_id.search_by_id(dict_data["id"])

                    if re_dict:
                        re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "OVER_MAXPAGE")
                
                elif music_platform == "Kugoumusic":
                    kugou = kugou_scrawl.Kugou()
                    re_dict = kugou.hash_search(dict_data["id"])

                    if re_dict:
                        re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "OVER_MAXPAGE")
                
                elif music_platform == "Kuwomusic":
                    kuwo = kuwo_scrawl.KuwoMusic()
                    re_dict = kuwo.Search_details(dict_data["id"])

                    if re_dict:
                        re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "OVER_MAXPAGE")

                elif music_platform == "Migumusic":
                    migu = migu_scrawl.Migu()
                    re_dict = migu.search_details(dict_data["id"])

                    if re_dict:
                        re_dict.update({"code":ReturnStatus.SUCCESS, "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code=ReturnStatus.OVER_MAXPAGE, status="Failed", detail = "OVER_MAXPAGE")

                elif music_platform == "Baidumusic":
                        baidu_search = baidu_scrawl.BaiduMusic()
                        re_dict      = baidu_search.search_by_id(song_id=dict_data["id"])


                else:
                    re_dict = _Return_Error_Post(code=ReturnStatus.NO_SUPPORT, status="Failed", detail = "NO_SUPPORT")
        finally:
                response = Response(json.dumps(re_dict), mimetype = 'application/json')    
                response.headers.add('Server','python flask')       
                response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
                response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
                return response

    else:
        re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_METHOD, status="Failed", detail = "ERROR_METHOD")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')      
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'         
        return response




@app.before_request
def redirect():
    if not request.path=='/' and request.path!='/get_token' and request.path!='/exist_token':
        try:
            token       = request.headers['token']
            token_value = Test_api(token)
            if token_value != 1:
                if token_value   == ReturnStatus.TOKEN_ERROR:
                    raise Error.Token_Time_Error()
                elif token_value == ReturnStatus.TOKEN_FORBED:
                    raise Error.Token_Contorl_Error()
        except Error.Token_Time_Error:
            re_dict  = _Return_Error_Post(code=ReturnStatus.TOKEN_ERROR, status="Failed", detail = "remind token")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')       
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        except Error.Token_Contorl_Error:
            re_dict  = _Return_Error_Post(code=ReturnStatus.TOKEN_FORBED, status="Failed", detail = "TOKEN_FORBED")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')       
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        except:
            re_dict  = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')       
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
            response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
            return response

        else:
            pass
    



# @app.route('/SpotifyLogin', methods=['GET', 'POST']) #登陆 并入以前的登陆接口 加入错误处理逻辑
# def SpotifyLogin():
#     if request.method == 'POST':
#         data          = request.get_data()
#         try:
#             dict_data = json.loads(data)
#             username  = dict_data['username']
#             password  = dict_data['password']
#         except KeyError:
#             re_dict   = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
#         except:
#             re_dict   = _Return_Error_Post(code=ReturnStatus.ERROR_UNKNOWN, status="Failed", detail = "ERROR_UNKNOWN")
#         else:
#             re_dict   = sp.login(username, password)
#         finally:
#             response  = Response(json.dumps(re_dict), mimetype='application/json')
#             response.headers.add('Server','python flask')       
#             response.headers['Access-Control-Allow-Origin'] = '*'
#             response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
#             response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
#             return response

#     else:
#         re_dict  = _Return_Error_Post(code=ReturnStatus.ERROR_METHOD, status="Failed", detail = "ERROR_METHOD")
#         response = Response(json.dumps(re_dict), mimetype = 'application/json')    
#         response.headers.add('Server','python flask')       
#         response.headers['Access-Control-Allow-Origin'] = '*'
#         response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
#         response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
#         return response




# @app.route('/SpotifyGoogle', methods=['GET', 'POST'])  #独立的 google 认证 加入错误处理逻辑 具体数据格式我和前端说
# def google():
#     if request.method == 'POST':
#         data = request.get_data()
#         try:
#             dict_data = json.loads(data)
#             username  = dict_data['username']
#             method    = dict_data['method']
#             nums      = dict_data['nums']
#         except KeyError:
#             re_dict   = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
#         except:
#             re_dict   = _Return_Error_Post(code=ReturnStatus.ERROR_UNKNOWN, status="Failed", detail = "ERROR_UNKNOWN")
#         else:

#             if method == 'mul_submit':
#                 re_dict = sp.mul_submit(username=username, nums=nums)
#             elif method == 'single_click':
#                 re_dict = sp.single_click(username=username, num=nums[0])
#             elif method == 'submit':
#                 re_dict = sp.submit(username=username)
#             else:
#                 re_dict = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS->MethodParams")
#             response    = Response(json.dumps(re_dict), mimetype = 'application/json')    
#             response.headers.add('Server','python flask')       
#             response.headers['Access-Control-Allow-Origin']  = '*'
#             response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
#             response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'            
#             return response
#     else:
#         re_dict  = _Return_Error_Post(code=ReturnStatus.ERROR_METHOD, status="Failed", detail = "ERROR_METHOD")
#         response = Response(json.dumps(re_dict), mimetype = 'application/json')    
#         response.headers.add('Server','python flask')       
#         response.headers['Access-Control-Allow-Origin']   = '*'
#         response.headers['Access-Control-Allow-Methods']  = 'OPTIONS,HEAD,GET,POST'
#         response.headers['Access-Control-Allow-Headers']  = 'x-requested-with'            
#         return response





# @app.route("/callback/") #这个路由不能改
# def callback():
#     """
#         后端的日志功能还不完善，所以暂时不修改异常写入
#     """
#     try:
#         error = request.args['error']
#         if error != None:
#             return error

#     except:
#         print('noerror') # 这里表示没有异常

#     try:
#         code  = request.args['code']
#         state = request.args['state']
#         sp.user_load_token(code, state)
#     except:
#         return 'error' # 按错误处理
#     return 'ok'




# @app.route("/SpotifyLogout") #注销函数 加入错误处理必要逻辑
# def SpotifyLogout():
#     try:
#         username = request.args['username']
#     except KeyError:
#         re_dict  = _Return_Error_Post(code=ReturnStatus.ERROR_PARAMS, status="Failed", detail = "ERROR_PARAMS")
#     else:
#         sp.user_login[username] = False
#         re_dict  = _Return_Error_Post(code=ReturnStatus.SUCCESS, status="SUCCESS", detail = "SUCCESS Logout")
#     finally:
#         response = Response(json.dumps(re_dict), mimetype = 'application/json')    
#         response.headers.add('Server','python flask')       
#         response.headers['Access-Control-Allow-Origin']   = '*'
#         response.headers['Access-Control-Allow-Methods']  = 'OPTIONS,HEAD,GET,POST'
#         response.headers['Access-Control-Allow-Headers']  = 'x-requested-with'            
#         return response





if __name__ == '__main__':
    """
    利用configparser库实现读取配置文件的功能
    这里是启用flask的debug模式
    """

    host = project.Config.config.getConfig("apptest", "apphost")
    port = project.Config.config.getConfig("apptest", "appport")
    app.run(host=host, port=int(port), debug = True)

