#!usr/bin/env python3
# @File:ip_proxies.py
# @Date:2018/2/10
# @UpDate_1:2018/2/27 凌晨.
# @UpDate_2:2018/2/28 凌晨.
# Author:Cat.1

import re, random, requests, time
import redis
import config.config

class Proxy_ip(object):

    def __init__(self):
        self.session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
                        'Referer': 'http://www.66ip.cn/areaindex_11/1.html'
                        }
        self.flag = 1
        if int(config.config.getConfig("open_database", "redis")) == 1:
            host              = config.config.getConfig("database", "dbhost")
            port              = config.config.getConfig("database", "dbport")
            self.r            = redis.Redis(host=host, port=int(port), decode_responses=True, db=4)  

    def download(self):
        global a
        try:
            num  = random.randint(1,10)
            if a == num:self.download()     # 解决由random引起的爬虫出错.
            url  = 'http://www.66ip.cn/areaindex_%s/3.html'%(num)
            # url = 'http://www.66ip.cn/areaindex_12/3.html'
            print('responsing -> %s'%(url))
            html = self.session.get(url, headers = self.headers)
        except:
            print('[-]get ip failed!')
            time.sleep(3)   # 系统休眠三秒钟进行爬虫适应.
            print('trying redownload...')
            a = num
            self.download() # 递归性的进行爬虫重新加载. 
        else:
            print('[+]get ip success!')
            content = html.content.decode('gbk')            # 数据清洗
            regex   = re.compile(r'<tr><td>([0-9.]+)')      
            ip      = regex.findall(content)
            regex   = re.compile(r'</td><td>([0-9.]+)</td><td>')
            dk      = regex.findall(content)
            test    = {}
            self.t  = {}
            for item in range(len(dk)):test[str(item)] = ip[item] + ':' + dk[item]
            test    = set(test.values())
            self.ip = 0
            for item in test:
                self.t[str(self.ip)] = item
                self.ip += 1

    def test_ip(self):      # 对获得的代理ip进行最后一次测试.
        self.success_ip = []
        for i in range(self.ip-1):
            proxies = {'http' : self.t[str(i)]}     # 组装代理ip成为dict可用形式.
            print(proxies)
            url     = 'http://www.baidu.com'
            try:
                print('[~]trying-response...')
                html = self.session.get(url, headers = self.headers, proxies = proxies, timeout = 5)
            except:
                print(proxies)
                print('[-]response failed!')
            else:
                print(proxies)
                print('[+]response success!')
                self.success_ip.append(proxies)
        print('[+]you have %d ip-address able!' %(len(self.success_ip)))
        for proxies in self.success_ip:
            try:html = self.session.get(url, headers = self.headers, proxies = proxies, timeout = 5)
            except:
                print('[-]ip failed!')
                z = 0
                for i in self.success_ip:   # 粗陋的办法去获取失败的ip在列表中的位置.
                    if i != proxies:z += 1
                    else:self.success_ip.pop(z) # 删除某一个失败的ip.
                del(z, i)       # 强迫症 -> 释放变量.
            else:print('[+]ip success!')

    def enter_SQL(self):
        dbsize = self.r.dbsize()
        num = len(self.success_ip)
        num_y = 0
        if num == 0:
            self.get_ip()
        for i in range(dbsize, dbsize+num):
            item = self.success_ip[num_y]
            print(item)
            self.r.set(str(i), item)
            num_y  += 1

    def fix_ip(self):
        while True:
            time.sleep(1800) # 时间为300秒为周期.
            self.r.flushdb()
            self.get_ip()

    def get_ip(self):           # 封装获取ip的办法.
        while self.flag == 1:   
            self.download()
            self.test_ip()
            self.enter_SQL()    # 
            self.flag = 0       # 修正标志位.



if __name__ == "__main__":
    get_ip = Proxy_ip()
    get_ip.get_ip()

    while True:         # 执行对数据库的ip的定期检测工作.
        get_ip.fix_ip() 

