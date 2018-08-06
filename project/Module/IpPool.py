import requests
import re
import redis

headers = {
        'Host': 'www.xicidaili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Referer': 'http://www.xicidaili.com/'
        }
r = redis.Redis(host=host, port=int(port), decode_responses=True)
ip_num = 100
page_num = 1

'''
设置ip池大小 默认50
'''
def set_ip_num(num):
    global ip_num
    ip_num = num * 2

'''
获取一个ip
返回值是一个字典{'ip':..., 'port':..., 'b':....}形式
'''
def get_ip():
    global page_num

    try:
        while r.scard('ip') <= ip_num / 2:
            if __add_ip(page_num) == 0:
                raise IOError
            page_num += 1

        ip_port = r.srandmember('ip', 1)[0]
        res = eval(ip_port.decode())
        res['b'] = ip_port
        return res
    except:
        return None

'''
删除一个ip
参数为 get_ip的返回值 res['b'] 
成功返回1 失败返回0
'''
def delete_ip(ip_port):
    global page_num
    try:
        res = r.srem('ip', ip_port)
        while r.scard('ip') <= ip_num / 2:
            if __add_ip(page_num) == 0:
                raise IOError
            page_num += 1
        return res
    except:
        return 0

'''
添加一页的ip 异常返回 0
'''
def __add_ip(page):
    try:
        url = 'http://www.xicidaili.com/nn/{0}'.format(page)
        response = requests.get(url, headers=headers)
        str = response.text
        result = re.finditer(pattern=r'<td>(\d+?.\d+?.\d+?.\d+?)</td>.*?<td>(\d+?)</td>.*?title="(.*?)秒"',
                             string=str, flags=re.DOTALL)
        result.__next__()  #判断一下是否为空
        for res in result:
            speed = float(res.group(3))
            if speed >= 1:
                continue
            ip_port = {'ip': res.group(1), 'port': res.group(2)}
            r.sadd("ip", ip_port)
            return 1
    except:
        return 0


if __name__ == '__main__':
    for i in range(1, 100):
        a = get_ip()
        print(a)
        if a!= None:
            print(a['ip'])
            delete_ip(a['b'])