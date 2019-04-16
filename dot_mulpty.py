# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 21:39:11 2019

@author: yifan
"""

from mpi4py import MPI
import time
import numpy as np
import random

N=2**20
x=[1,2,3]*(N//3)
y=[1,-2,1]*(N//3)

def dot_mul(x:'List[float]',y:'List[float]')->'float':
    sum=0
    for i in range(len(x)):
        sum+=x[i]*y[i]
    return float(sum)

if __name__=='__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    t0=MPI.Wtime()
#    print('my rank:',rank)
    res=np.zeros(1)
    step=N//size
    tmp_x=x[rank*step:(rank+1)*step]
    tmp_y=y[rank*step:(rank+1)*step]
    value=dot_mul(tmp_x,tmp_y)
    value=value*np.ones(1)
    comm.Reduce(value,res,root=0,op=MPI.SUM)
    if rank==0:
        print('the res is:%f'%res)
        print('the time is:%f'%(MPI.Wtime()-t0))
#    print('the time is:%f',MPI.Wtime())
#    if rank==0:
#        result+=value
#        for i in range(1,size):
#            data=comm.recv(source=i,tag=0)
#            result+=data
#        t1=time.time()
#        print('the value is:%d,\n,the time is:%f'%(result,t1-t0))
#    else:
#        comm.send(value,dest=0,tag=0)
            
        