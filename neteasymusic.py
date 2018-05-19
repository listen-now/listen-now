#!usr/bin/env python3
# @File:Neteasymusic.py
# @Date:2018/5/9
# Author:Cat.1

from flask import Flask,request,Response,jsonify
import json, time
import AES, scrawl_Neteasymusic, scrawl_Xiamimusic, scrawl_QQmusic
import config

re_dict = {}
app = Flask(__name__)
# 形成flask实例

@app.route('/')
def hello_world():
    return 'Hello World!  This is ZhuYuefeng\'s test_api.  Thanks your requests.  Cat.1'

@app.route('/search', methods = ['POST', 'GET'])
def search_json():
    global re_dict
    if request.method == 'POST':
        re_dict = {}
        data      = request.get_data()      # 获得json数据包.
        try:
            dict_data = json.loads(data)        # 解析json数据包.
        except:
            re_dict = {"code":"405", "status":"Failed", "detail":"post not json_data!"}
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            # 组装数据包成json格式返回
            response.headers.add('Server','python flask')       
            # 增加信息头内容.
            return response
        try:
            music_title    = dict_data["title"]
            music_platform = dict_data["platform"]
            try:
                music_page     = dict_data["page"]
            except:
                music_page = 1
            # 获得请求的歌曲名字和选择的音乐平台
        except:
            re_dict = {"code":"404", "status":"Failed"} 
            # 反馈字段不完整的报错状态码.
        else:
            if music_page > 10:
                re_dict = {"code":"403", "status":"Failed", "detail":"Is so many response!"} 
            else:
                if music_title != '' or music_title != None:
                    if music_platform == "Neteasymusic":
                        neteasymusic_id = scrawl_Neteasymusic.Netmusic()
                        print(music_title)
                        re_dict         = neteasymusic_id.pre_response_neteasymusic(music_title, music_page)
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success"})
                            # 组装成功接收的状态码.    
                        else:
                            re_dict = {"code":"403", "status":"Failed"}
                    elif music_platform == "Xiamimusic":
                        print("Xiamimusic")
                        xiamimusic_id = scrawl_Xiamimusic.Search_xiami()
                        re_dict       = xiamimusic_id.search_xiami(music_title, music_page)                        
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success"})
                        # 组装成功接收的状态码.    
                        else:
                            re_dict = {"code":"403", "status":"Failed"}
                    elif music_platform == "QQmusic":
                        print("QQmusic")
                        qqmusic_id = scrawl_QQmusic.Qqmusic()
                        re_dict    = qqmusic_id.qq_music_search(music_title, music_page)                        
                        print(re_dict)
                        if re_dict:
                            re_dict.update({"code":"200", "status":"Success"})
                        # 组装成功接收的状态码.    
                        else:
                            re_dict = {"code":"403", "status":"Failed"}

                    else:
                        re_dict = {"code":"406", "status":"Failed", "detail":"Not know platform!"}                         
                else:
                    re_dict = {"code":"404", "status":"Failed"} 
                    # 反馈字段不完整的报错状态码.
        finally:
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            # 组装数据包成json格式返回
            response.headers.add('Server','python flask')       
            # 增加信息头内容.
            return response
    else:
        re_dict  = {"code":"400", "status":"Failed"}
        # 返回请求错误(应该为post请求而非get)的状态码400
        response = Response(json.dumps(re_dict), mimetype = 'application/json')
        response.headers.add('Server','python flask')
        return response

@app.route('/id', methods = ['POST', 'GET'])
def play_id():
    global re_dict
    if request.method == 'POST':
        data      = request.get_data()      # 获得json数据包.
        dict_data = json.loads(data)        # 解析json数据包.
        try:
            music_id       = dict_data["id"]
            music_platform = dict_data['platform']
            # 获得请求的歌曲id和选择的音乐平台
        except:
            re_dict = {"code":"404", "status":"Failed"} 
            # 反馈字段不完整的报错状态码404.
        else:
            if music_id != '' or music_id != None:
                if music_platform == "Neteasymusic":
                    neteasymusic_id = scrawl_Neteasymusic.Netmusic()
                    re_dict = neteasymusic_id.music_id_requests(music_id)
                    if re_dict:
                        re_dict.update({"code":"200", "status":"Success"})
                        # 组装成功接收的状态码200.        
                    else:
                        re_dict = {"code":"401", "status":"Failed", "detail":"post not json_data!"}
                        # 返回该平台没有歌曲的状态码401

                elif music_platform == "Xiamimusic":
                    re_dict = scrawl_Xiamimusic.id_search(music_id)
                    # print(re_dict)
                    if re_dict:
                        re_dict.update({"code":"200", "status":"Success"})
                        # 组装成功接收的状态码.    
                    else:
                        re_dict = {"code":"403", "status":"Failed"}

                elif music_platform == "QQmusic":
                    qqmusic_id = scrawl_QQmusic.Qqmusic()
                    re_dict = qqmusic_id.access_resp_text(dict_data["media_mid"], dict_data["songmid"])
                    # print(re_dict)
                    # 注意检测media_mid、songmid参数的合法情况.
                    if re_dict:
                        re_dict.update({"code":"200", "status":"Success"})
                        # 组装成功接收的状态码.    
                    else:
                        re_dict = {"code":"403", "status":"Failed"}
                else:
                    re_dict = {"code":"406", "status":"Failed", "detail":"Not know platform!"}                         
        finally:
            response = Response(json.dumps(re_dict), mimetype = 'application/json')    
            # 组装数据包成json格式返回
            response.headers.add('Server','python flask')       
            # 增加信息头内容.
            return response
    else:
        re_dict  = {"code":"400", "status":"Failed"}
        # 返回请求错误(应该为post请求而非get)的状态码400
        response = Response(json.dumps(re_dict), mimetype = 'application/json')
        response.headers.add('Server','python flask')
        return response


if __name__ == '__main__':
    host = config.getConfig("apptest", "apphost")
    port = config.getConfig("apptest", "appport")
    app.run(host=host, port=port, debug = True)

