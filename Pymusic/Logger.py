#!/usr/bin/env python3
# @File:Logger.py
# @Date:2018/06/06
# Author:Cat.1


import logging
from logging import handlers


class Logger(object):
    """
    代码参考自https://www.cnblogs.com/nancyzhu/p/8551506.html
    自其介绍如何创建一个可以向文件、并向终端输出日志的脚本
    
    Logger类用于向终端、文件(可指定*.log)中输出你的日志信息
    因为利用了logging库, 故可选的输出的日志信息有: 
                                            1.debug 最低版本(以下所有均会输出)
                                            2.info  输出除了debug...(输出正常信息)
                                            3.输出最低级为警告信息
                                            4.输出最低级为错误信息
                                            5.严重错误, 表明软件已不能继续运行了

    通过初始化Logger类, 设定参数即可使用该日志脚本
    """

    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'critical':logging.CRITICAL
    }

    def __init__(self, filename, level='info', when='D', backCount=10, format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        
        self.logger = logging.getLogger(filename)

        format_str = logging.Formatter(format)# 设置日志格式
        self.logger.setLevel(self.level_relations.get(level))# 设置日志级别
        sh = logging.StreamHandler()# 往屏幕上输出
        sh.setFormatter(format_str) # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒, M 分, H 小时, D 天, W 每星期（interval==0时代表星期一）, midnight 每天凌晨
        
        th.setFormatter(format_str)
        # 设置文件里写入的格式
        self.logger.addHandler(sh) 
        # 把对象加到logger里
        self.logger.addHandler(th)

if __name__ == '__main__':

    
    log = Logger('all.log',level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')


    # Logger('error.log', level='error').logger.error('error')