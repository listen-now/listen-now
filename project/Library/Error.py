#!usr/bin/env python3
# @File:Error.py
# @Date:2018/08/03
# @Update:2018/08/30
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

class ReturnFunction(Exception):

    def __init__(self, ErrorString):
        self.ErrorString = ErrorString
        Exception.__init__(self)

    def __str__(self):
        return ("[-]" + self.ErrorString)

class ReturnFuncParams(ReturnFunction):
    pass

class ReturnFuncType(ReturnFunction):
    pass


if __name__ == '__main__':

    raise ReturnFuncParams("This is an Error")
    # ReturnFunction("This is an Error", "Params_Error")









