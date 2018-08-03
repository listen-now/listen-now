#!usr/bin/env python3
# @File:Error.py
# @Date:2018/8/3
# Author:Cat.1



class Token_Time_Error(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return ("[-]Token Time Error!")

class Token_Contorl_Error(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return ("[-]Token Contorl Error")

class Params_Error(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return ("[-]Params Error")
