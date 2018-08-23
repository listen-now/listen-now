# __fileName__ : SpotifyMusic.py
# __date__ : 2018/08/21
# __author__ : ZhangQi


import copy
import threading
from selenium import webdriver
import urllib.parse as urllibparse
import time
import requests
import re
import spotipy
import spotipy.oauth2 as oauth2
import RetDataModule
import ReturnStatus
import random
import json

#常量
IMG_PATH = '/SpotifyMeta'

STR_REGEX = r'<div class="rc-imageselect-desc.*?" style=".*?">(.*?)<strong style=".*?">(.*?)</strong>(.*?)<span.*?>(.*?)</span>'
IMG_REGEX = r'<td role="button" tabindex="0" class="rc-imageselect-tile".*?><div class="rc-image-tile-target">.*?src="(.*?)"'

CLIENT_ID = '1aae9cd374db4058a5fa8612ab5662c2'
CLIENT_SECRET = 'a1eaf40664494397922e575e870e771f'

SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')

SCOPE = "playlist-modify-public playlist-modify-private user-library-read"
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8081
REDIRECT_URI = "{}:{}/callback/".format(CLIENT_SIDE_URL, PORT)

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "state": '#####state#####',
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

access_data = {
    'grant_type': 'authorization_code',
    'code': '',
    'redirect_uri': REDIRECT_URI,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET

}

refresh_data = {
    'grant_type': 'refresh_token',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'refresh_token': ''
}

SOMETHING = ["{}={}".format(key, urllibparse.quote(val)) for key, val in list(auth_query_parameters.items())]
URL_ARGS = "&".join(SOMETHING)

AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)
#常量

class Spotify(object):
    pre_drivers = []                     #待使用的驱动
    pre_drivers_lock = threading.Lock()  #待使用的驱动锁
    used_drivers = {}                    #已使用驱动
    used_drivers_lock = threading.Lock() #已使用驱动锁
    img_urls = {}                        #9 或 8张图片时每个图片的url 用户名:图片url列表
    state_user = {}                      #用户与 state 的绑定
    user_access_token = {}               #用户 access_token
    user_refresh_token = {}              #用户 refresh_token
    user_login = {}                      #用户的登陆状态

    credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)  #要生成token的东西
    spot = spotipy.Spotify(auth=credentials.get_access_token())
    token = ''


    '''
        :param d_num: 驱动的数量
        初始化几个待用的驱动为了防止token过期 每3分钟删一个
    '''
    def __init__(self, d_num):
        pass
        loadd = threading.Thread(target=self.load_driver, args=[d_num])
        loadd.start()
        removet = threading.Thread(target=self.remove_driver)
        removet.start()
        loadt = threading.Thread(target=self.load_token)
        loadt.start()


    '''
        加载待用驱动
    '''
    def load_driver(self, d_num):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        while True:
            if len(self.pre_drivers) < d_num:
                driver = webdriver.Chrome(chrome_options=options)
                state = str(random.randint(0,999999999))
                repl = AUTH_URL.replace(urllibparse.quote('#####state#####'), state)
                driver.get(repl)
                try:
                    driver.find_element_by_link_text('BEI SPOTIFY ANMELDEN').click()
                except:
                    driver.find_element_by_link_text('LOG IN TO SPOTIEY').click()
                self.pre_drivers_lock.acquire()
                try:
                    self.pre_drivers.append({'driver': driver, 'state': state})
                finally:
                    self.pre_drivers_lock.release()


    '''
        定时删除驱动
    '''
    def remove_driver(self):
        while True:
            time.sleep(1000)
            if len(self.pre_drivers) > 0:
                self.pre_drivers_lock.acquire()
                try:
                    self.pre_drivers.pop(0)
                finally:
                    self.pre_drivers_lock.release()

    '''
        定时加载token
    '''
    def load_token(self):
        while True:
            self.token = self.credentials.get_access_token()
            self.spot = spotipy.Spotify(auth=self.token)
            time.sleep(3000)

    '''
        刷新token
    '''
    def refresh_token(self):
        self.token = self.credentials.get_access_token()
        self.spot = spotipy.Spotify(auth=self.token)

    '''
        获取用户的两个token
    '''
    def user_load_token(self, code, state):
        try:
            access_data['code'] = code
            res = requests.post(url='https://accounts.spotify.com/api/token',
                                data=access_data).text
            res = json.loads(res)
            username = self.state_user[state]
            self.user_access_token[username] = res['access_token']
            self.user_refresh_token[username] = res['refresh_token']
            self.user_login[username] = True
            refresh_token = threading.Thread(target=self.user_refresh_token_m, args=[username])
            refresh_token.start()
        except:
            return

    '''
        刷新用户token
    '''
    def user_refresh_token_m(self, username):
        while self.user_login[username]:
            refresh_data['refresh_token'] = self.user_refresh_token[username]
            res = requests.post(url='https://accounts.spotify.com/api/token',
                                data=refresh_data, ).text
            res = json.loads(res)
            self.user_access_token[username] = res['access_token']
            time.sleep(3000)

    '''
        登陆 输入用户名和密码
        返回的是 1. google人机认证的操作描述 前端要显示出来
                 2. google人机认证的图片块数 人机认证一共有两种方式 
                 一种 A 是选出全部符合描述的图片并提交 (图片块数为16张)
                 一种 B 是一次点一张符合描述的图片直到没有符合描述的图片时点提交 (图片块数为是8张或9张)
                 3. 用户名 以后关于认证的请求都要带上用户名
        随后前端要请求一张静态图片 人机识别的图片 图片是一整张 前端要根据块数把图片切割开
        16张的4×4 1:1 9张的3×3 1:1 8张的4×2 4行两列 1:2 分开之后的图片宽是长的两倍
    '''
    def login(self, username, password):
        #取预先准备好的驱动
        self.pre_drivers_lock.acquire()
        try:
            driver_state = self.pre_drivers.pop(0)
        finally:
            self.pre_drivers_lock.release()

        #绑定驱动与 state
        driver = driver_state['driver']
        state = driver_state['state']
        self.state_user[str(state)] = username

        #将驱动放入已使用驱动
        self.used_drivers_lock.acquire()
        try:
            self.used_drivers.update({username: driver})
        finally:
            self.used_drivers_lock.release()

        name_elem = driver.find_element_by_name('username')
        pasw_elem = driver.find_element_by_name('password')
        name_elem.send_keys(username)
        pasw_elem.send_keys(password)

        # 点击登陆并调整到 google人机
        driver.find_element_by_id('login-button').click()
        page_source = driver.page_source
        res = re.search(pattern=r'<div style="visibility:.*?name="(.*?)"', string=page_source)
        astr = res.group(1)
        driver.switch_to.frame(astr)

        # 这里要等待切换完成
        time.sleep(1)

        # 寻找提示字符串
        pattern = STR_REGEX
        res = re.search(pattern=pattern, string=page_source)
        restr = res.group(1) + res.group(2) + res.group(3) + res.group(4) # 要返回的字符串

        # 寻找图片
        pattern = IMG_REGEX
        res = re.search(pattern=pattern, string=page_source)
        # 图片地址 调整转义
        img_url = res.group(1)
        img_url = img_url.replace('amp;', '')
        # 请求图片并保存
        reqs = requests.get(url=IMG_PATH + img_url)
        filename = username + '.png'
        with open(filename, 'wb') as f:
            f.write(reqs.content)

        #计算图片块个数
        elems = driver.find_elements_by_class_name('rc-image-tile-wrapper')
        elems_len = len(elems)

        # 9 或 8时储存每张图片的url
        if elems_len == 8 or elems_len == 9:
            urls = []
            for x in range(0, elems_len):
                urls.append(img_url)
            self.img_urls[username] = urls

        re_dict = {}
        re_dict['descrstr'] = restr #描述字符串
        re_dict['username'] = username #用户名
        re_dict['imgnum'] = elems_len #图片的数量
        return re_dict


    '''
        点击多个并提交
    '''
    def mul_submit(self, username, nums):
        # 获取用户的驱动
        self.used_drivers_lock.acquire()
        try:
            driver = self.used_drivers[username]
        finally:
            self.used_drivers_lock.release()

        # 获取以前的图片链接
        page_source = driver.page_source
        pattern = IMG_REGEX
        res = re.search(pattern=pattern, string=page_source)
        prev_img = res.group(1)
        curr_img = prev_img

        # 点击图片并提交
        elems = driver.find_elements_by_class_name('rc-image-tile-wrapper')
        for num in nums:
            elems[num].click()
        driver.find_element_by_id('recaptcha-verify-button').click()

        # 获取当前的图片链接
        while curr_img == prev_img:
            page_source = driver.page_source
            pattern = IMG_REGEX
            res = re.search(pattern=pattern, string=page_source)
            curr_img = res.group(1)

        # 存入当前图片
        curr_img = curr_img.replace('amp;', '')
        reqs = requests.get(url=IMG_PATH + curr_img)
        filename = username + '.png'
        with open(filename, 'wb') as f:
            f.write(reqs.content)

        # 寻找提示字符串
        pattern = STR_REGEX
        res = re.search(pattern=pattern, string=page_source)
        restr = res.group(1) + res.group(2) + res.group(3) + res.group(4)  # 要返回的字符串

        # 计算图片块个数
        elems = driver.find_elements_by_class_name('rc-image-tile-wrapper')
        elems_len = len(elems)

        # 9 或 8时储存每张图片的url
        if elems_len == 8 or elems_len == 9:
            urls = []
            for x in range(0, elems_len):
                urls.append(curr_img)
            self.img_urls[username] = urls

        re_dict = {}
        re_dict['descrstr'] = restr
        re_dict['imgnum'] = elems_len  # 图片的数量
        return re_dict

    '''
        点击单个图片
    '''
    def single_click(self, username, num):
        # 获取用户的驱动
        self.used_drivers_lock.acquire()
        try:
            driver = self.used_drivers[username]
        finally:
            self.used_drivers_lock.release()

        # 获取以前的图片链接
        prev_img = self.img_urls[username][num]
        curr_img = prev_img

        # 点击
        elems = driver.find_elements_by_class_name('rc-image-tile-wrapper')
        elems[num].click()
        driver.find_element_by_id('recaptcha-verify-button').click()

        # 现在图片的url
        while curr_img == prev_img:
            page_source = driver.page_source
            pattern = IMG_REGEX
            res = re.finditer(pattern=pattern, string=page_source)
            i = 0
            for ress in res:
                if i == num:
                    curr_img = ress.group(1)
                    curr_img = curr_img.replace('amp;', '')
                i = i + 1

        # 存入当前图片
        reqs = requests.get(url=IMG_PATH + curr_img)
        filename = username + str(num) + '.png'
        with open(filename, 'wb') as f:
            f.write(reqs.content)

        re_dict = {}
        re_dict['imgnum'] = num
        return re_dict

    '''
        提交
    '''
    def submit(self, username):
        # 获取用户的驱动
        self.used_drivers_lock.acquire()
        try:
            driver = self.used_drivers[username]
        finally:
            self.used_drivers_lock.release()

        #点击之前的描述
        page_source = driver.page_source
        pattern = STR_REGEX
        res = re.search(pattern=pattern, string=page_source)
        prev_str = res.group(1) + res.group(2) + res.group(3) + res.group(4)
        curr_str = prev_str

        #点击提交
        driver.find_element_by_id('recaptcha-verify-button').click()

        #查看是否要重试
        while prev_str == curr_str:
            page_source = driver.page_source
            pattern = STR_REGEX
            try:
                res = re.search(pattern=pattern, string=page_source)
                curr_str = res.group(1) + res.group(2) + res.group(3) + res.group(4)
            except:
                #不需要重试
                return curr_str

        #需要重试 存图片
        pattern = IMG_REGEX
        res = re.search(pattern=pattern, string=page_source)
        img_url = res.group(1)
        img_url = img_url.replace('amp;', '')
        reqs = requests.get(url=img_url)
        filename = username + '.png'
        with open(filename, 'wb') as f:
            f.write(reqs.content)

        # 计算图片块个数
        elems = driver.find_elements_by_class_name('rc-image-tile-wrapper')
        elems_len = len(elems)

        # 9 或 8时储存每张图片的url
        if elems_len == 8 or elems_len == 9:
            urls = []
            for x in range(0, elems_len):
                urls.append(img_url)
            self.img_urls[username] = urls

        re_dict = {}
        re_dict['descrstr'] = curr_str
        re_dict['imgnum'] = elems_len  # 图片的数量
        return re_dict

    '''
        根据歌名搜索音乐
        :keyword 歌名
        :page 页数
        :num 每页的歌曲数
    '''
    def search_by_keyword(self, keyword, page=1, num=10):
        re_dict = copy.deepcopy(RetDataModule.mod_search)

        try:
            res = self.spot.search(q=keyword, limit=num, offset=((page-1)*num))
        except:
            self.refresh_token()
            try:
                res = self.spot.search(q=keyword, limit=num, offset=((page-1) * num))
            except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
                return re_dict

        try:
            re_dict['now_page'] = page
            re_dict['next_page'] = page + 1
            re_dict['before_page'] = page - 1

            for x in range(0, num):
                tmp_song = copy.deepcopy(RetDataModule.mod_song)
                tmp_song['music_id'] = res['tracks']['items'][x]['id']
                tmp_song['music_name'] = res['tracks']['items'][x]['name']
                tmp_song['artists'] = res['tracks']['items'][x]['artists'][0]['name']
                tmp_song['image_url'] = res['tracks']['items'][x]['album']['images'][2]['url']
                re_dict['song']['list'].append(copy.deepcopy(tmp_song))
                re_dict['song']['totalnum'] += 1
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
            re_dict['status'] = 'ERROR_UNKNOWN'

        return re_dict

    '''
        根据id搜索歌曲
        :music_id 歌曲的id
    '''
    def search_by_id(self, music_id):
        re_dict = copy.deepcopy(RetDataModule.mod_search)

        try:
            res = self.spot.track(music_id)
        except:
            self.refresh_token()
            try:
                res = self.spot.track(music_id)
            except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
                return re_dict

        try:
            tmp_song = copy.deepcopy(RetDataModule.mod_song)
            tmp_song['music_id'] = res['id']
            tmp_song['music_name'] = res['name']
            tmp_song['artists'] = res['artists'][0]['name']
            tmp_song['image_url'] = res['album']['images'][2]['url']
            re_dict['song']['list'].append(copy.deepcopy(tmp_song))
            re_dict['song']['totalnum'] += 1
            re_dict['next_page'] = 1
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
            re_dict['status'] = 'ERROR_UNKNOWN'

        return re_dict

    '''
        返回推荐歌单
        这里只返回歌单信息 没有返回歌曲信息
        :num 返回的歌单数
    '''
    def get_playlist(self, num):

        re_dict = copy.deepcopy(RetDataModule.mod_dissidlist)

        try:
            res = self.spot.featured_playlists(limit=num)
        except:
            self.refresh_token()
            try:
                res = self.spot.featured_playlists(limit=num)
            except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
                return re_dict

        try:
            for x in range(0, len(res['playlists']['items'])):
                tmp_list = copy.deepcopy(RetDataModule.mod_cdlist)
                tmp_list['dissid'] = res['playlists']['items'][x]['id']
                tmp_list['dissname'] = res['playlists']['items'][x]['name']
                tmp_list['nickname'] = tmp_list['dissname']
                tmp_list['image_url'] = res['playlists']['items'][x]['images'][0]['url']
                re_dict['list'].append(tmp_list)
                re_dict['totaldiss'] += 1
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
            re_dict['status'] = 'ERROR_UNKNOWN'

        return re_dict

    '''
        根据歌单id获取歌单详情
        :playlist_id 歌单id
    '''
    def get_playlist_inf(self, playlist_id):
        re_dict = copy.deepcopy(RetDataModule.mod_cdlist)

        try:
            res = requests.get(url='https://api.spotify.com/v1/playlists/{}'.format(playlist_id),
                               headers = {'authorization': 'Bearer {}'.format(self.token)}).text
        except:
            self.refresh_token()
            try:
                res = requests.get(url='https://api.spotify.com/v1/playlists/{}'.format(playlist_id),
                                   headers={'authorization': 'Bearer {}'.format(self.token)}).text
            except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
                return re_dict

        res = json.loads(res)

        try:
            re_dict['dissid'] = res['id']
            re_dict['dissname'] = res['name']
            re_dict['nickname'] = re_dict['dissname']
            re_dict['info'] = res['description']
            re_dict['image_url'] = res['images'][0]['url']
            track_num = len(res['tracks'])
            for x in range(0, track_num):
                tmp_song = copy.deepcopy(RetDataModule.mod_song)
                tmp_song['music_id'] = res['tracks']['items'][x]['track']['id']
                tmp_song['music_name'] = res['tracks']['items'][x]['track']['name']
                tmp_song['artists'] = res['tracks']['items'][x]['track']['artists'][0]['name']
                tmp_song['image_url'] = res['tracks']['items'][x]['track']['album']['images'][2]['url']
                re_dict['song']['list'].append(tmp_song)
                re_dict['song']['totalnum'] += 1
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
            re_dict['status'] = 'ERROR_UNKNOWN'

        return re_dict

    '''
        返回所有主题
    '''
    def get_mod_hot_item_list(self):
        re_dict = copy.deepcopy(RetDataModule.mod_hot_item_list)

        try:
            res = self.spot.categories(limit=35)
        except:
            self.refresh_token()
            try:
                res = self.spot.categories(limit=35)
            except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
                return re_dict

        try:
            for x in range(0, 35):
                tmp_item = copy.deepcopy(RetDataModule.mod_hot_item)
                tmp_item['item_id'] = res['categories']['items'][x]['id']
                tmp_item['item_name'] = res['categories']['items'][x]['name']
                tmp_item['item_desc'] = ''
                re_dict['itemlist'].append(tmp_item)
                re_dict['totalitem'] += 1
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
            re_dict['status'] = 'ERROR_UNKNOWN'
        return re_dict

    '''
        返回某个主题下的几个歌单
        :itemid 主题id
        :num 要返回的歌单数量
    '''

    def get_item_playlist(self, itemid, num):
        re_dict = copy.deepcopy(RetDataModule.mod_hot_dissid_list)

        try:
            res = self.spot.category_playlists(category_id=itemid, limit=num)
        except:
            self.refresh_token()
            try:
                res = self.spot.category_playlists(category_id=itemid, limit=num)
            except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
                return re_dict

        try:
            for x in range(0, len(res['playlists']['items'])):
                re_dict['idlist'].append(res['playlists']['items'][x]['id'])
                re_dict['totaldiss'] += 1
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
            re_dict['status'] = 'ERROR_UNKNOWN'
        return re_dict

    '''
        获取用户收藏音乐
    '''
    def get_user_track(self, username):
        re_dict = copy.deepcopy(RetDataModule.mod_cdlist)

        if not self.user_login[username]:
            re_dict['code'] = ReturnStatus.USER_FAILED_SIGN_IN
            re_dict['status'] = 'ERROR_NOT_SIGN_IN'
            return re_dict

        try:
            res = requests.get(url='https://api.spotify.com/v1/me/tracks',
                               headers={'authorization': 'Bearer {}'.format(self.user_access_token[username])}
                               ).text
        except:
            self.refresh_token()
            try:
                res = requests.get(url='https://api.spotify.com/v1/me/tracks',
                                   headers={'authorization': 'Bearer {}'.format(self.user_access_token[username])}
                                   ).text
            except:
                re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
                re_dict['status'] = 'ERROR_UNKNOWN'
                return re_dict

        res = json.loads(res)

        try:
            track_num = len(res['items'])
            for x in range(0, track_num):
                tmp_song = copy.deepcopy(RetDataModule.mod_song)
                tmp_song['music_id'] = res['items'][x]['track']['id']
                tmp_song['music_name'] = res['items'][x]['track']['name']
                tmp_song['artists'] = res['items'][x]['track']['artists'][0]['name']
                tmp_song['image_url'] = res['items'][x]['track']['album']['images'][2]['url']
                re_dict['song']['list'].append(tmp_song)
                re_dict['song']['totalnum'] += 1
        except:
            re_dict['code'] = ReturnStatus.ERROR_UNKNOWN
            re_dict['status'] = 'ERROR_UNKNOWN'


        return re_dict


