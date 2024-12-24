# coding=utf-8

"""
@fileName       :   server.py
@data           :   2024/8/28
@author         :   jiangmenggui@hosonsoft.com
"""
from datetime import datetime
from lljz_tools.decorators import debug 

@debug
def f1(n):
    for i in range(n):
        pass 

@debug
def f2(n):
    for i in range(n):
        datetime.now()    
    


if __name__ == '__main__':
    f1(100000)
    f2(100000)
