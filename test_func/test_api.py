#!/usr/bin/env python3
# @File:test_api.py
# @Date:2018/05/27
# Author:Cat.1

import json
import requests
import unittest
import time

class TestDict(unittest.TestCase):
    """
    用于后端整个系统的单元测试脚本    
    """
    def post_func(self, my_dict, p):
        """发送post请求
        
        主要用于抽象出发送post请求的函数 
        
        Arguments:
            my_dict {dict} -- 接收dict封装的json数据包
            p {str} -- 接受str用于构造url访问地址
        
        Returns:
            返回 -- 返回服务器返回的json数据
        """
        my_dict = json.dumps(my_dict)
        url = "http://127.0.0.1:8888/" + p
        return requests.post(url, data = my_dict)


    def get_func(self, p):
        """发送get请求
        
        主要抽象出发送get请求的函数
        
        Arguments:
            p {str} -- 接受p用于构造访问地点
        
        Returns:
            返回 -- get请求数据包
        """
        url = "http://127.0.0.1:8888/" + p
        return requests.get(url)


    def test_search(self):
        """单元测试模块(搜索api)
        
        搜索api的单元测试模块, 包括Neteasymusic、Xiamimusic、QQmusic
        以及页数测试
        """
        my_dict =  {
                    "title":"成都",
                    "platform":None,
                    "page":1
                    }

        test_platform = [
                         "Neteasymusic", 
                         "Xiamimusic", 
                         "QQmusic",
                        ]


        for i in test_platform:
            my_dict["platform"] = i
            self.assertEqual(json.loads(self.post_func(my_dict, "search").text)['code'], "200")
            my_dict["page"] = 1
            self.assertEqual(json.loads(self.post_func(my_dict, "search").text)['code'], "200")
            time.sleep(1)

        my_dict["page"]  = 10
        my_dict["title"] = "白金迪斯科"
        with self.assertRaises(KeyError):
            self.assertEqual(json.loads(self.post_func(my_dict, "search").text)['code'], "200")


    def test_id_net_xiami(self):
        my_dict       = {
                         "id":None,
                         "platform":None,
                        }

        my_dict["id"]       = 444706287
        my_dict["platform"] = "Neteasymusic"
        self.assertEqual(json.loads(self.post_func(my_dict, "id").text)['code'], "200")
        my_dict["id"]       = 123456
        my_dict["platform"] = "Xiamimusic"
        self.assertEqual(json.loads(self.post_func(my_dict, "id").text)['code'], "200")


    def test_check_user(self):
        pass

    def test_Return_Random_User_Song_List(self):
        self.assertEqual(len(json.loads(self.get_func("Random_song_list").text)), 8)




if __name__ == '__main__':
    unittest.main()




# nohup uwsgi --emperor  /home/zhuyuefeng/flask-file-uploader/ &
