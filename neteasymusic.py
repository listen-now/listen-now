#!usr/bin/env python3
# @File:Neteasymusic.py
# @Date:2018/5/9
# Author:Cat.1
# 2018/05.20 代码重构

from flask import Flask,request,Response,jsonify
import json, time
import AES
import scrawl_Neteasymusic
import scrawl_Xiamimusic
import scrawl_QQmusic
import config
import Hot_Song_List
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

def _Return_Error_Post(code, status, detail = ""):
    """
    用于向前端反馈错误信息的函数
    包括code参数 错误码
    status 状态信息
    detail 相信信息
    组装数据包成json格式返回
    """
    return {"code":code, "status":status, "detail":detail}




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
                        neteasymusic_id = scrawl_Neteasymusic.Netmusic()
                        re_dict         = neteasymusic_id.pre_response_neteasymusic(music_title, music_page)
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")
                    elif music_platform == "Xiamimusic":
                        xiamimusic_id = scrawl_Xiamimusic.Search_xiami()
                        re_dict       = xiamimusic_id.search_xiami(music_title, music_page)                        
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")
                    elif music_platform == "QQmusic":
                        qqmusic_id = scrawl_QQmusic.Qqmusic()
                        re_dict    = qqmusic_id.qq_music_search(music_title, music_page)                        
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success"})
                        else:
                            re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")

                    else:
                        re_dict = _Return_Error_Post(code="406", status="Failed", detail = "Not know platform!")

                else:
                    re_dict = _Return_Error_Post(code="404", status="Failed", detail = "")
        finally:
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            response.headers.add('Server','python flask')       
            return response

    else:
        re_dict = _Return_Error_Post(code="400", status="Failed", detail = "")
        response = Response(json.dumps(re_dict), mimetype = 'application/json')    
        response.headers.add('Server','python flask')       
        return response

@app.route('/user_song_list', methods = ['POST', 'GET'])
def Return_Random_User_Song_List():

    global re_dict
    return_user_song_list = Hot_Song_List.Hot_Song_List()
    re_dict = return_user_song_list.Random_Return_func()
    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
    response.headers.add('Server','python flask')       
    return response

@app.route('/song_list_requests', methods = ['POST', 'GET'])
def Return_User_Song_List_Detail():

    global re_dict
    data = request.get_data()      # 获得json数据包.
    try:
        dict_data = json.loads(data)        # 解析json数据包.
    except:
        re_dict = _Return_Error_Post(code="405", status="Failed", detail = "post not json_data!")

    try:
        song_list_url   = dict_data["url"]
    except:
        re_dict = _Return_Error_Post(code="404", status="Failed", detail = "")
    else:
        return_user_song_list = Hot_Song_List.Hot_Song_List()
        re_dict = return_user_song_list.top_songlist(song_list_url)
    response = Response(json.dumps(re_dict), mimetype = 'application/json')    
    response.headers.add('Server','python flask')       
    return response



@app.route('/id', methods = ['POST', 'GET'])
def play_id():
    """
    用于前端请求歌曲id/media_mid、songmid 时服务器针对性的反馈方法
    基本内容如上, 如果请求的是网易/虾米则会检测id信息,
    QQ音乐则会检测media_mid、songmid值.
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
            if music_id != '' or music_id != None:
                if music_platform == "Neteasymusic":
                    neteasymusic_id = scrawl_Neteasymusic.Netmusic()
                    music_id        = dict_data["id"]
                    re_dict         = neteasymusic_id.music_id_requests(music_id)
                    if re_dict:
                        re_dict.update({"code":"200", "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code="401", status="Failed", detail = "platform not this music!")
                elif music_platform == "Xiamimusic":
                    music_id = dict_data["id"]
                    re_dict  = scrawl_Xiamimusic.id_search(music_id)
                    if re_dict:
                        re_dict.update({"code":"200", "status":"Success"})
                    else:
                        re_dict = _Return_Error_Post(code="403", status="Failed", detail = "")

                elif music_platform == "QQmusic":
                    qqmusic_id = scrawl_QQmusic.Qqmusic()
                    re_dict = qqmusic_id.access_resp_text(dict_data["media_mid"], dict_data["songmid"])
                    # print(re_dict)
                    # 注意检测media_mid、songmid参数的合法情况.
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
    host = config.getConfig("apptest", "apphost")
    port = config.getConfig("apptest", "appport")
    app.run(host=host, port=int(port), debug = True)

