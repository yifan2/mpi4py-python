# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 19:06:12 2019

@author: yifan
"""

from mpi4py import MPI
import time
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def calculate_part(start, step):
    sum=0.0
    flag=1
    for i in range(0,step):
        if(start % 2 != 0):
            flag=-1
        else:
            flag=1
        sum+=flag * (1/(2*start+1))
        start +=1

    return sum
    
N = 1024*1024*64
t0=time.time()#计算串行时间
value=calculate_part(0,N)*4
t1=time.time()
print('the pi value is:,the time is:',value,t1-t0)
#sum=np.zeros((1,))
#step = N // size
#start = rank * step
#t0=time.time()
#value = calculate_part(start, step)*np.ones((1,))
#comm.Reduce(value,sum, op=MPI.SUM)
#t1=time.time()
#print('the time is:',t1-t0)
#print('the value is:',sum)

#if __name__=='__main__':
#    result=0
#    t1=MPI.Wtime()
#    step = N // size
#    start = rank * step
#    value=calculate_part(start,step)
#    if rank == 0:
#        result += value
#        for i in range(1,size):
#            value = comm.recv(source=i, tag=0)
#            result += value
#        print('PI is : ',result * 4)
#        print('time cost is', MPI.Wtime() - t1, 's')
#        
#    else:
#        comm.send(value, dest=0, tag=0)