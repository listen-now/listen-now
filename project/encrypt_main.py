#!/usr/bin/env python3
import sys #line:7
sys .path .append ('..')#line:8
import copy #line:9
from flask import Flask ,request ,Response ,jsonify #line:10
import json ,time #line:11
import re #line:12
from Scrawl .NeteasyMusic import NeteasyMusic as neteasy_scrawl #line:13
from Scrawl .XiamiMusic import XiamiMusic as xiami_scrawl #line:14
from Scrawl .QQMusic import QQMusic as qq_scrawl #line:15
import Config .config #line:16
from Sync .NeteasySync import Hot_Song_List as neteasy_Hot_Song_List #line:17
from Sync .NeteasySync import Neteasymusic_Sync #line:18
from project .Module import ReturnStatus #line:19
from project .Module import RetDataModule #line:20
from project .Helper import bcrypt_hash #line:21
from Sync .XiamiSync import XiamiMusic as xiami_Song_List #line:22
"""
引入json网页框架用于开放api接口
引入json库用于解析前端上传的json文件
引入AES外部文件用于加密网易云音乐的POST数据
引入scrawl_Neteasymusic、scrawl_Xiamimusic、scrawl_QQmusic用于各个平台的爬虫
引入config文件用于配置数据库等配置信息
"""#line:30
re_dict ={}#line:32
app =Flask (__name__ )#line:33
@app .route ('/')#line:37
def hello_world ():#line:38
    ""#line:41
    return 'Hello World!  This is ZhuYuefeng\'s test_api.  Thanks your requests.  Cat.1'#line:42
def _OO000O00O000OOOO0 (OO00OOOO0000OO0OO ,OOOOOOO00O0O0OO00 ,detail ="",**OOOO0OOO00O0O00OO ):#line:44
    ""#line:51
    return {"code":OO00OOOO0000OO0OO ,"status":OOOOOOO00O0O0OO00 ,"detail":detail ,"other":OOOO0OOO00O0O00OO }#line:52
@app .route ('/search',methods =['POST','GET'])#line:57
def search_json ():#line:58
    ""#line:65
    global re_dict #line:66
    if request .method =='POST':#line:67
        re_dict ={}#line:68
        OOOOOO00O000OO00O =request .get_data ()#line:69
        try :#line:70
            OO00OOO0OOO000000 =json .loads (OOOOOO00O000OO00O )#line:71
        except :#line:72
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PSOT_DATA ,status ="Failed",detail ="post not json_data!")#line:73
        try :#line:74
            OOO0O0000OOOOOO00 =OO00OOO0OOO000000 ["title"]#line:75
            OO0OOO000O0000OO0 =OO00OOO0OOO000000 ["platform"]#line:76
            try :#line:77
                O0O00OOOO0000OOOO =OO00OOO0OOO000000 ["page"]#line:78
            except :#line:79
                O0O00OOOO0000OOOO =1 #line:80
        except :#line:82
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:83
        else :#line:84
            if O0O00OOOO0000OOOO >10 :#line:85
                re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .OVER_MAXPAGE ,status ="Failed",detail ="Is so many response!")#line:86
            else :#line:88
                if OOO0O0000OOOOOO00 !=''or OOO0O0000OOOOOO00 !=None :#line:89
                    if OO0OOO000O0000OO0 =="Neteasymusic":#line:90
                        OOO0O00OO00O00000 =neteasy_scrawl .Netmusic ()#line:91
                        re_dict =OOO0O00OO00O00000 .pre_response_neteasymusic (OOO0O0000OOOOOO00 ,O0O00OOOO0000OOOO )#line:92
                        try :#line:93
                            re_dict ["code"]#line:94
                        except KeyError :#line:95
                            if re_dict :#line:96
                                re_dict .update ({"code":ReturnStatus .SUCCESS ,"status":"Success","now_page":O0O00OOOO0000OOOO ,"next_page":O0O00OOOO0000OOOO +1 ,"before_page":O0O00OOOO0000OOOO -1 })#line:97
                            else :#line:98
                                re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .OVER_MAXPAGE ,status ="Failed",detail ="")#line:99
                        else :#line:100
                            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_SEVER ,status ="Failed",detail ="")#line:101
                    elif OO0OOO000O0000OO0 =="Xiamimusic":#line:103
                        OO00OO0OO00O00000 =xiami_scrawl .Search_xiami ()#line:104
                        re_dict =OO00OO0OO00O00000 .search_xiami (OOO0O0000OOOOOO00 ,O0O00OOOO0000OOOO )#line:105
                        if re_dict :#line:106
                            re_dict .update ({"code":ReturnStatus .SUCCESS ,"status":"Success","now_page":O0O00OOOO0000OOOO ,"next_page":O0O00OOOO0000OOOO +1 ,"before_page":O0O00OOOO0000OOOO -1 })#line:107
                        else :#line:108
                            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .OVER_MAXPAGE ,status ="Failed",detail ="")#line:109
                    elif OO0OOO000O0000OO0 =="QQmusic":#line:110
                        O0O0OOOO00O00OO00 =qq_scrawl .QQMusic ()#line:112
                        re_dict =O0O0OOOO00O00OO00 .search_by_keyword (OOO0O0000OOOOOO00 ,O0O00OOOO0000OOOO )#line:113
                        try :#line:114
                            re_dict ["code"]#line:115
                        except KeyError :#line:116
                            if re_dict :#line:117
                                re_dict .update ({"code":ReturnStatus .SUCCESS ,"status":"Success","now_page":O0O00OOOO0000OOOO ,"next_page":O0O00OOOO0000OOOO +1 ,"before_page":O0O00OOOO0000OOOO -1 })#line:118
                            else :#line:119
                                re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .OVER_MAXPAGE ,status ="Failed",detail ="")#line:120
                        else :#line:121
                            pass #line:122
                    else :#line:123
                        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .NO_SUPPORT ,status ="Failed",detail ="Not know platform!")#line:124
                else :#line:126
                    re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:127
        finally :#line:128
            if re_dict =="":#line:129
                re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .NOT_SAFE ,status ="Failed",detail ="Unknown Error!")#line:130
            O00O0OO0O0O00O0O0 =Response (json .dumps (re_dict ),mimetype ='application/json')#line:132
            O00O0OO0O0O00O0O0 .headers .add ('Server','python flask')#line:133
            return O00O0OO0O0O00O0O0 #line:134
    else :#line:136
        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_METHOD ,status ="Failed",detail ="")#line:137
        O00O0OO0O0O00O0O0 =Response (json .dumps (re_dict ),mimetype ='application/json')#line:138
        O00O0OO0O0O00O0O0 .headers .add ('Server','python flask')#line:139
        return O00O0OO0O0O00O0O0 #line:140
@app .route ('/Random_song_list',methods =['POST'])#line:142
def Return_Random_User_Song_List ():#line:143
    ""#line:148
    global re_dict #line:149
    if request .method =="POST":#line:150
        OO0O000000OOOOO0O =request .get_data ()#line:151
        try :#line:152
            OO00OO0O00OOO0OO0 =json .loads (OO0O000000OOOOO0O )#line:153
        except :#line:154
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PSOT_DATA ,status ="Failed",detail ="post not json_data!")#line:155
        OO00O00OOOOO0OOOO =OO00OO0O00OOO0OO0 ["platform"]#line:156
        if OO00O00OOOOO0OOOO =="Neteasymusic":#line:157
            if int (Config .config .getConfig ("open_database","redis"))==1 :#line:158
                OO000OO0OOOO00000 =neteasy_Hot_Song_List .Hot_Song_List ()#line:159
                re_dict =OO000OO0OOOO00000 .Random_Return_func ()#line:160
                if re_dict :#line:161
                    re_dict .update ({"code":ReturnStatus .SUCCESS ,"status":"Success"})#line:162
                else :#line:163
                    re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .NOT_SAFE ,status ="Failed",detail ="Unknown Error!")#line:164
                OOOOO0OO0OOO00OOO =Response (json .dumps (re_dict ),mimetype ='application/json')#line:165
                OOOOO0OO0OOO00OOO .headers .add ('Server','python flask')#line:166
                return OOOOO0OO0OOO00OOO #line:167
            else :#line:168
                re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .DATABASE_OFF ,status ="Failed",detail ="数据库未启用")#line:169
                OOOOO0OO0OOO00OOO =Response (json .dumps (re_dict ),mimetype ='application/json')#line:170
                OOOOO0OO0OOO00OOO .headers .add ('Server','python flask')#line:171
            return OOOOO0OO0OOO00OOO #line:172
        else :#line:173
            pass #line:175
    else :#line:176
        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_METHOD ,status ="Failed",detail ="")#line:177
        OOOOO0OO0OOO00OOO =Response (json .dumps (re_dict ),mimetype ='application/json')#line:178
        OOOOO0OO0OOO00OOO .headers .add ('Server','python flask')#line:179
        return OOOOO0OO0OOO00OOO #line:180
@app .route ('/login',methods =["POST"])#line:182
def login ():#line:183
    ""#line:192
    global re_dict #line:193
    OO0O0O0OO0O0000OO =request .get_data ()#line:195
    try :#line:196
        OOOO0O0OO0O00OO0O =json .loads (OO0O0O0OO0O0000OO )#line:197
    except :#line:198
        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PSOT_DATA ,status ="Failed",detail ="post not json_data!")#line:199
    if re .findall (r"wechat",request .headers .get ("User-Agent")):#line:201
        try :#line:202
            O0O0000OO0O0O00OO =OOOO0O0OO0O00OO0O ["open_id"]#line:203
            O00O0O0000000O0O0 ="Wechat_Mini_Program"#line:204
        except :#line:205
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:206
    else :#line:208
        try :#line:209
            O0O0000OO0O0O00OO =OOOO0O0OO0O00OO0O ["user_id"]#line:210
            O00O0O0000000O0O0 =OOOO0O0OO0O00OO0O ["passwd"]#line:211
        except :#line:212
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:213
    try :#line:214
        OO00O0OOO00O00O0O =OOOO0O0OO0O00OO0O ["flag"]#line:215
    except :OO00O0OOO00O00O0O =1 #line:216
    if OO00O0OOO00O00O0O :#line:217
        OOO0O0O0OOOO00O00 =bcrypt_hash .Sign_In_Check (O0O0000OO0O0O00OO ,O00O0O0000000O0O0 )#line:218
        if OOO0O0O0OOOO00O00 ["code"]==ReturnStatus .USER_SUCCESS_SIGN_IN or OOO0O0O0OOOO00O00 ["code"]==ReturnStatus .USER_WECHAT_SIGN :#line:219
            re_dict =copy .deepcopy (OOO0O0O0OOOO00O00 )#line:221
        elif OOO0O0O0OOOO00O00 ["code"]==ReturnStatus .USER_FAILED_SIGN_IN :#line:223
            re_dict =copy .deepcopy (OOO0O0O0OOOO00O00 )#line:224
        elif OOO0O0O0OOOO00O00 ["code"]==ReturnStatus .USER_NOT_SIGN_UP :#line:225
            re_dict =copy .deepcopy (OOO0O0O0OOOO00O00 )#line:226
    OO0O000O00000O0OO =Response (json .dumps (re_dict ),mimetype ='application/json')#line:231
    OO0O000O00000O0OO .headers .add ('Server','python flask')#line:232
    return OO0O000O00000O0OO #line:233
@app .route ('/user_song_list',methods =['POST','GET'])#line:239
def Return_User_Song_List ():#line:240
    ""#line:245
    global re_dict #line:246
    O0O0O0O0OO00000OO =request .get_data ()#line:247
    try :#line:248
        OO000OOOOO00O0000 =json .loads (O0O0O0O0OO00000OO )#line:249
    except :#line:250
        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PSOT_DATA ,status ="Failed",detail ="post not json_data!")#line:251
    if re .findall (r"wechat",request .headers .get ("User-Agent")):#line:253
        try :#line:254
            OOOO0O00O0000O000 =OO000OOOOO00O0000 ["open_id"]#line:255
        except :#line:256
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:257
    else :#line:259
        try :#line:260
            OOOO0O00O0000O000 =OO000OOOOO00O0000 ["user_id"]#line:261
        except :#line:262
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .USER_NOT_SIGN_IN ,status ="Failed",detail ="用户未注册")#line:263
        else :#line:264
            pass #line:265
    if OOOO0O00O0000O000 !=None :#line:266
        try :#line:267
            OO0000OO0O0OO0OOO =OO000OOOOO00O0000 ["uid"]#line:268
            OO0OO000O0OO00OO0 =OO000OOOOO00O0000 ["platform"]#line:269
        except :#line:270
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:271
        else :#line:272
            if OO0OO000O0OO00OO0 =="Neteasymusic":#line:273
                OO000O000O00O0000 =Neteasymusic_Sync .Neteasymusic_Sync ()#line:274
                re_dict =OO000O000O00O0000 .Get_User_List (OO0000OO0O0OO0OOO ,OOOO0O00O0000O000 )#line:275
            elif OO0OO000O0OO00OO0 =="QQmusic":#line:276
                OO000O000O00O0000 =qq_scrawl .QQMusic ()#line:277
                re_dict =OO000O000O00O0000 .Get_User_List (OO0000OO0O0OO0OOO ,OOOO0O00O0000O000 )#line:278
        if re_dict :#line:279
            re_dict .update ({"code":"202","status":"Success"})#line:280
        else :#line:281
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_SEVER ,status ="Failed",detail ="")#line:282
    O00O000O000OOO000 =Response (json .dumps (re_dict ),mimetype ='application/json')#line:283
    O00O000O000OOO000 .headers .add ('Server','python flask')#line:284
    return O00O000O000OOO000 #line:285
@app .route ('/song_list_requests',methods =['POST','GET'])#line:288
def Return_User_Song_List_Detail ():#line:289
    ""#line:298
    global re_dict #line:299
    O0OOO0O0O00O00O00 =request .get_data ()#line:300
    try :#line:301
        O0O0O0OO0O0O00OO0 =json .loads (O0OOO0O0O00O00O00 )#line:302
    except :#line:303
        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PSOT_DATA ,status ="Failed",detail ="post not json_data!")#line:304
    try :#line:306
        O0OO00O00000OO00O =O0O0O0OO0O0O00OO0 ["platform"]#line:307
    except :#line:308
        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:309
    else :#line:310
        if O0OO00O00000OO00O =="Neteasymusic":#line:311
            OO000OOOO0OO00OOO =O0O0O0OO0O0O00OO0 ["url"]#line:312
            O0OO00O0OOOOOOO00 =neteasy_Hot_Song_List .Hot_Song_List ()#line:313
            re_dict =O0OO00O0OOOOOOO00 .Download_SongList (OO000OOOO0OO00OOO )#line:314
        elif O0OO00O00000OO00O =="QQmusic":#line:315
            O00O000OO00OOO000 =O0O0O0OO0O0O00OO0 ["id"]#line:316
            O0OO00O0OOOOOOO00 =qq_scrawl .QQMusic ()#line:317
            re_dict =O0OO00O0OOOOOOO00 .get_cdlist (disstid =O00O000OO00OOO000 )#line:318
            re_dict =O0OO00O0OOOOOOO00 .Download_SongList (OO000OOOO0OO00OOO )#line:319
        elif O0OO00O00000OO00O =="Xiamimusic":#line:321
            O0OOOO00OO000OOO0 =xiami_Song_List .XiamiApi ()#line:322
            re_dict =retrun_song_list .getPlaylist (OO000OOOO0OO00OOO )#line:323
        if re_dict :#line:325
            re_dict .update (_OO000O00O000OOOO0 (code =ReturnStatus .SUCCESS ,status ="Success",detail ="None"))#line:326
        else :#line:327
            re_dict .update (_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_SEVER ,status ="Failed",detail ="没有更多数据或服务器发生错误"))#line:328
    O0O000O0OOOOOOO00 =Response (json .dumps (re_dict ),mimetype ='application/json')#line:330
    O0O000O0OOOOOOO00 .headers .add ('Server','python flask')#line:331
    return O0O000O0OOOOOOO00 #line:332
@app .route ('/check_user',methods =['GET','POST'])#line:334
def check_user ():#line:335
    O00O0OOOOOO000000 ={}#line:336
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
    """#line:347
    if request .method =="POST":#line:348
        O0OOOOO0000OOOO00 =request .get_data ()#line:349
        try :#line:351
            OO000OOO000O0OO00 =json .loads (O0OOOOO0000OOOO00 )#line:352
        except :#line:353
            O00O0OOOOOO000000 =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PSOT_DATA ,status ="Failed",detail ="POST not json_data!")#line:354
            OO0OO0O0O0OO0OO0O =Response (json .dumps (O00O0OOOOOO000000 ),mimetype ='application/json')#line:355
            OO0OO0O0O0OO0OO0O .headers .add ('Server','python flask')#line:356
            return OO0OO0O0O0OO0OO0O #line:357
        if re .findall (r"wechat",request .headers .get ("User-Agent")):#line:359
            try :#line:360
                O0O0OOOOO00OOOOOO =OO000OOO000O0OO00 ["open_id"]#line:361
                OOOOO0OO00OO00O00 ="Wechat_Mini_Program"#line:362
            except :#line:363
                O00O0OOOOOO000000 =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:364
        else :#line:366
            O0O0OOOOO00OOOOOO =OO000OOO000O0OO00 ["user_id"]#line:367
            OOOOO0OO00OO00O00 =OO000OOO000O0OO00 ["passwd"]#line:368
        try :#line:369
            O0O0OOO0OO0O0OO0O =OO000OOO000O0OO00 ["flag"]#line:370
        except :O0O0OOO0OO0O0OO0O =1 #line:371
        if O0O0OOO0OO0O0OO0O :#line:372
            OO0OOOO0OOO00OOOO =bcrypt_hash .Sign_In_Check (O0O0OOOOO00OOOOOO ,OOOOO0OO00OO00O00 )#line:373
            if OO0OOOO0OOO00OOOO ["code"]==ReturnStatus .USER_SUCCESS_SIGN_IN or OO0OOOO0OOO00OOOO ["code"]==ReturnStatus .USER_WECHAT_SIGN :#line:374
                pass #line:376
    elif request .method =="GET":#line:378
        pass #line:379
    else :#line:381
        O00O0OOOOOO000000 =_OO000O00O000OOOO0 (code =ReturnStatus .DATABASE_OFF ,status ="Failed",detail ="数据库繁忙或遇到技术障碍")#line:382
        OO0OO0O0O0OO0OO0O =Response (json .dumps (O00O0OOOOOO000000 ),mimetype ='application/json')#line:383
        OO0OO0O0O0OO0OO0O .headers .add ('Server','python flask')#line:384
        return OO0OO0O0O0OO0OO0O #line:385
@app .route ('/id',methods =['POST','GET'])#line:389
def play_id ():#line:390
    ""#line:394
    global re_dict #line:395
    if request .method =='POST':#line:396
        O0OOOO0O00O0OO00O =request .get_data ()#line:397
        OOO00O0000O000O0O =json .loads (O0OOOO0O00O0OO00O )#line:398
        try :#line:399
            OO00OOOO0O0OO0O0O =OOO00O0000O000O0O ['platform']#line:400
        except :#line:401
            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:402
        else :#line:403
            if OO00OOOO0O0OO0O0O !=''or OO00OOOO0O0OO0O0O !=None :#line:404
                if OO00OOOO0O0OO0O0O =="Neteasymusic":#line:405
                    OOO0OO0000O0O0O0O =neteasy_scrawl .Netmusic ()#line:407
                    O0O0O000OOOOO0O00 =OOO00O0000O000O0O ["id"]#line:408
                    re_dict =OOO0OO0000O0O0O0O .music_id_requests (O0O0O000OOOOO0O00 )#line:409
                    if re_dict :#line:410
                        re_dict .update ({"code":ReturnStatus .SUCCESS ,"status":"Success"})#line:411
                    else :#line:412
                        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .NO_MUSIC_DETAIL ,status ="Failed",detail ="platform not this music!")#line:413
                elif OO00OOOO0O0OO0O0O =="Xiamimusic":#line:414
                    try :#line:415
                        O0O0O000OOOOO0O00 =OOO00O0000O000O0O ["id"]#line:416
                    except KeyError :#line:417
                        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_PARAMS ,status ="Failed",detail ="")#line:418
                    else :#line:419
                        re_dict =xiami_scrawl .Search_xiami .id_req (O0O0O000OOOOO0O00 )#line:420
                        print (re_dict )#line:421
                        if re_dict :#line:422
                            re_dict .update ({"code":ReturnStatus .SUCCESS ,"status":"Success"})#line:423
                        else :#line:424
                            re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .OVER_MAXPAGE ,status ="Failed",detail ="")#line:425
                elif OO00OOOO0O0OO0O0O =="QQmusic":#line:427
                    OOO0000O00O0O0000 =qq_scrawl .QQMusic ()#line:428
                    re_dict =OOO0000O00O0O0000 .search_by_id (OOO00O0000O000O0O ["id"])#line:429
                    if re_dict :#line:431
                        re_dict .update ({"code":ReturnStatus .SUCCESS ,"status":"Success"})#line:432
                    else :#line:433
                        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .OVER_MAXPAGE ,status ="Failed",detail ="")#line:434
                else :#line:435
                    re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .NO_SUPPORT ,status ="Failed",detail ="Not know platform!")#line:436
        finally :#line:437
                OOO0O000O000OOOOO =Response (json .dumps (re_dict ),mimetype ='application/json')#line:438
                OOO0O000O000OOOOO .headers .add ('Server','python flask')#line:439
                return OOO0O000O000OOOOO #line:440
    else :#line:442
        re_dict =_OO000O00O000OOOO0 (code =ReturnStatus .ERROR_METHOD ,status ="Failed",detail ="")#line:443
        OOO0O000O000OOOOO =Response (json .dumps (re_dict ),mimetype ='application/json')#line:444
        OOO0O000O000OOOOO .headers .add ('Server','python flask')#line:445
        return OOO0O000O000OOOOO #line:446
if __name__ =='__main__':#line:451
    """
    利用configparser库实现读取配置文件的功能
    这里是启用flask的debug模式
    """#line:455
    host =Config .config .getConfig ("apptest","apphost")#line:456
    port =Config .config .getConfig ("apptest","appport")#line:457
    app .run (host =host ,port =int (port ),debug =True )#line:458
