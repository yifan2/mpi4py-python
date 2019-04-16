# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 23:16:09 2019

@author: yifan
"""

from mpi4py import MPI
import numpy as np
import os
import time

def gen_data(m,n,p):
    A=np.zeros([m,n])
    B=np.zeros([n,p])
    for i in range(m):
        for j in range(n):
            A[i,j]=i+j
    for k in range(n):
        for l in range(p):
            B[k,l]=i+j
    return A,B

def matrix_mul(mat1,mat2):
    m,n=mat1.shape[0],mat2.shape[1]
    C=np.zeros([m,n])
    mat2=np.transpose(mat2)
    for i in range(m):
        for j in range(n):
            C[i,j]=np.dot(mat1[i,:],mat2[j,:])
    return C

if __name__=='__main__':
#    t1=time.time() #串行算法时间
#    A,B=gen_data(2000,1000,2000)
#    C=matrix_mul(A,B)
#    t2=time.time()
#    print('the time is',t2-t1)
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print('my rank is',rank)
    
    t1=MPI.Wtime()
    if rank==0:
        A,B=gen_data(20,10,200)
        group=A.shape[0]//size
        tmp=[]
        for i in range(size-1):
            tmp.append(A[group*i:group*(i+1),:])
        tmp.append(A[group*(size-1):,:])
    else:
        tmp,B=None,None
    recv_A=comm.scatter(tmp,root=0)
    recv_B=comm.bcast(B,root=0)
    tmp_c=matrix_mul(recv_A,recv_B)
    result=comm.gather(tmp_c,root=0)
    if rank==0:
        result=np.vstack(result)
        t2=MPI.Wtime()
        print(result.shape)
        print('the time is:',t2-t1)
    