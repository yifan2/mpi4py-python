# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:10:35 2019

@author: yifan
"""

import multiprocessing

def foo(i):
    print ('called function in process: %s' %i)
    return

if __name__ == '__main__':
    Process_jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=foo, args=(i,))
        Process_jobs.append(p)
        p.start()
        p.join()
        
        
#import multiprocessing 
#import target_function
#if __name__ == '__main__':
#    Process_jobs = []
#    for i in range(5):
#        p = multiprocessing.Process(target=target_function.function,args=(i,))
#        Process_jobs.append(p)
#        p.start()
#        p.join()