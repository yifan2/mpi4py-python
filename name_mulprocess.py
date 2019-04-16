# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:15:15 2019

@author: yifan
"""

import multiprocessing
import time

def foo():
    name = multiprocessing.current_process().name
    print("Starting %s \n" % name)
    time.sleep(3)
    print("Exiting %s \n" % name)

if __name__ == '__main__':
    process_with_name = multiprocessing.Process(name='foo_process', target=foo)
#    process_with_name.daemon = True  # 注意原代码有这一行，但是译者发现删掉这一行才能得到正确输出
    process_with_default_name = multiprocessing.Process(target=foo)
    process_with_name.start()
    process_with_default_name.start()