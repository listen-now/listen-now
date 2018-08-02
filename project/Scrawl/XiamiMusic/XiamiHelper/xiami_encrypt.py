#!usr/bin/env python3
# @File:Xiami_encrypt.py
# @Date:2018/5/10
# Author:Cat.1


import urllib.parse

def xiami_encrypt(text):
    url = text
    h = url[:1]
    # 行数
    url = url[1:]
    # url信息
    h_len = round(len(url)/int(h))
    # 每行的数量
    new_url = ''
    for z in range(h_len):        
        q = 0
        for i in range(int(h)):
            try:
                new_url_ = url[q:q+h_len]
                new_url  += new_url_[z]
                q += h_len
            except IndexError:
                pass
    return urllib.parse.unquote(new_url).replace('^', '0')

if __name__ == '__main__':

    url = "4h%2F8an213135%79357.%uk326%555ce81Ec31ct3Fm.meF%3%3E263_E6m3teD6%5EEE3389db65tA%1xit828273F8666_pFhy155E---3a7%2c94p%22i.%2F2F%1195%8l3a_%52E%%%d7fe5ed8c"
    print(xiami_encrypt(url))
    