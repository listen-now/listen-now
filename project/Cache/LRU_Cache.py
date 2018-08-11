#!/usr/bin/env python3
# @File:LRU_Cache.py
# @Date:2018/08/08
# Author:Cat.1

import sys
sys.path.append('..') # 必须要, 设置project为源程序的包顶
import copy
from Module import RetDataModule


# encoding:utf-8
import io  
import sys  
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 


class LRUCache(object):




    class Node(object):



        def __init__(self, key, value):

            self.key                = key

            self.value              = copy.deepcopy(value)
            self.next               = None
            self.prev               = None

        def print_value(self):
            print(self.value)
            # for item in self.value:
            #     print(item, self.value[item])

    def __init__(self, capacity=10000):

        self.head       = self.Node(None, None)
        self.tail       = self.Node(None, None)
        self.head.next  = self.tail
        self.tail.prev  = self.head
        self.__length   = 0
        self.capacity   = capacity
        self.dict_table = {}


    def isEmpty(self):
        self.__length = 0



    def length(self):
        return self.__length


    def insert(self, node):
        # 每次插入都从最前面插入
        if self.tail.prev.value == None:

            link           = self.head.next
            self.head.next = node
            node.prev      = self.head
            node.next      = link
            self.tail.prev = node
        else:
            link           = self.head.next
            self.head.next = node
            node.prev      = self.head
            node.next      = link
            link.prev      = node



    def remove(self, node):
        # 移除的时候分为，在dict_table中，则移除中间的node，然后在第一个地方再插入；否则直接插入在双向链表最前面即可

        prevNode      = node.prev
        nextNode      = node.next
        prevNode.next = nextNode
        nextNode.prev = prevNode



    def set(self, key, value):

        if self.__length >= self.capacity: # 如果目前的链表中数据大于最大限制
            if key in self.dict_table:
                removeNode = self.dict_table[key]
                removeKeyNode = removeNode.key
                self.remove(removeNode)
                self.__length -= 1
                self.dict_table.pop(removeKeyNode)
            else:            
                removeNode = self.tail.prev
                removeKeyNode = removeNode.key
                self.remove(removeNode)
                self.__length -= 1
                self.dict_table.pop(removeKeyNode)

        newNode = self.Node(key, value)
        self.insert(newNode)
        self.dict_table.update({key:newNode})
        self.__length += 1
        return 1


    def get(self, key):

        if key in self.dict_table: # 确认请求的数据在双向链表里面
            node = self.dict_table[key]
            self.remove(node)
            self.insert(node)
            return node.value # 返回请求的数据
        else:
            return -1 # 返回链表里没有该数据

    def creatNode(self, key, play_url, music_id, music_name, artists, image_url, lyric, comment):
        node = copy.deepcopy(RetDataModule.mod_song)
        node["play_url"]   = play_url
        node["music_id"]   = music_id
        node["music_name"] = music_name
        node["artists"]    = artists
        node["image_url"]  = image_url
        node["lyric"]      = lyric
        node["comment"]    = comment

        return node

if __name__ == '__main__':

    test = LRUCache()
    
    node = test.creatNode("NEM123456", "http://play_url.zlclclc.cn", 123456, "浮夸", "陈奕迅", "http://image.zlclclc.cn", "This is lyric", ["This is comment(s)"])
    test.set("NEM123456", node)

    node = test.creatNode("NEM123789", "http://play_url.zlclclc.cn", 123789, "十年", "陈奕迅", "http://image.zlclclc.cn", "This is lyric", ["This is comment(s)"])
    test.set("NEM123789", node)

    node = test.creatNode("NEM567123", "http://play_url.zlclclc.cn", 567123, "纸短情长", "花粥", "http://image.zlclclc.cn", "This is lyric", ["This is comment(s)"])
    test.set("NEM567123", node)

    node = test.creatNode("NEM987123", "http://play_url.zlclclc.cn", 987123, "九九八十一", "纪久川", "http://image.zlclclc.cn", "This is lyric", ["This is comment(s)"])
    test.set("NEM987123", node)

    node = test.creatNode("NEM123789", "http://play_url.zlclclc.cn", 123789, "十年", "陈奕迅", "http://image.zlclclc.cn", "This is lyric", ["This is comment(s)"])
    test.set("NEM123789", node)


    print(test.head.value)
    print(test.head.next.value)
    print(test.head.next.next.value)
    print(test.head.next.next.next.value)



