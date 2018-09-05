# 引用关系说明
    此目录下的工作目录中的代码文件若要引用根目录模块,需要添加根目录路径
    添加方式:
        import sys
        sys.path.append('../..')
    代码解释:
        导入模块sys
        首先上级目录为Scrwal, ..表示
        Scrawl上级目录为根目录, ..表示
        最后../..表示根目录
    用例说明:
        QQMusic.py爬虫返回数据要用根目录下的Module中的模块:
            RetDataModule #返回json数据模版
            ReturnStatus #返回数据状态码模版
        1.然后先添加根目录
        2.导入Module:
            from Module import RetDataModule #导入返回json数据模版
            from Module import ReturnStatus #导入返回数据状态码模版
        3.导入其他采用相同方式:
            from Library import *
            from Helper import *
            from ... import ...
