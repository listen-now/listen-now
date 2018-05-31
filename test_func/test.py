#!/usr/bin/env python3
# @File:sjakhdh.py
# @Date:FileDate
# Author:Cat.1

import requests
import asyncio
import aiohttp
# @asyncio.coroutine
# def hello():
#     print("Hello world!")
#     # 异步调用asyncio.sleep(1):
#     r = yield from asyncio.sleep(10)
#     print("Hello again!")

# # 获取EventLoop:
# loop = asyncio.get_event_loop()
# # 执行coroutine
# loop.run_until_complete(hello())
# loop.close()

@asyncio.coroutine
def print_page(url):
    response = yield from aiohttp.request('GET', url)
    body = yield from response.read_and_close(decode=True)
    print(body)


loop = asyncio.get_event_loop()
loop.run_until_complete(print_page('http://www.baidu.com'))