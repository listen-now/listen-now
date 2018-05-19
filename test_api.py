import json
import requests
# # encoding:utf-8
# import io  
# import sys  
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 


my_dict = {
    # "id":444706287,
    "title":"白金迪斯科",
    "platform":"Neteasymusic"
}

my_dict = json.dumps(my_dict)
# # print(my_dict)
# url = "http://www.zlclclc.cn/search"
# test = requests.post(url, data = my_dict)
# print(json.loads(test.text))
a = 1
c = a == 1
print(type(c))
# nohup uwsgi --emperor  /home/zhuyuefeng/flask-file-uploader/ &
