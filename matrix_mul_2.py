# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 09:46:46 2019

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
            B[k,l]=k+l
    return A,B

def matrix_mul(mat1,mat2):
    m,n=mat1.shape[0],mat2.shape[0]
#    m,n=len(mat1),len(mat2)
    C=np.zeros([m,n])
#    mat2=np.transpose(mat2)
    for i in range(m):
        for j in range(n):
            C[i,j]=np.dot(mat1[i,:],mat2[j,:])
    return C
#res=np.zeros([2000,2000])
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
print('my rank is',rank)

if __name__=='__main__':
    t1=MPI.Wtime()
    if rank==0:
        tmp1,tmp2=gen_data(20,10,20)
        tmp2=np.transpose(tmp2)
        A=[]
        B=[]
        group1=tmp1.shape[0]//size
        group2=tmp2.shape[0]//size
        for i in range(size-1):
            A.append(tmp1[group1*i:group1*(i+1),:])
            B.append(tmp2[group2*i:group2*(i+1),:])
        A.append(tmp1[group1*size:,:])
        B.append(tmp2[group2*size:,:])
    else:
        A,B=None,None
    tmp=[None]*size
    A_rank=comm.scatter(A,root=0)
    B_rank=comm.scatter(B,root=0)
#    print(A_rank.shape,B_rank.shape)
    tmp[rank]=matrix_mul(A_rank,B_rank)
    cicle=0
    for cicle in range(size):
        if cicle!=rank:
            col=(cicle+rank)%size
#            data=comm.sendrecv(B_rank,dest=rank,source=cicle)
#            req=comm.Isend(B_rank,dest=cicle,tag=rank+cicle)
            comm.send(B_rank,dest=cicle,tag=rank+cicle)
#            req.wait()
            comm.barrier()
#            buf=bytearray(1<<20)
#            req2=comm.Irecv(buf,source=cicle,tag=cicle+rank)
            data=comm.recv(source=cicle,tag=cicle+rank)
#            data=req2.wait()
#            print(cicle)
#            print(data)
            tmp=matrix_mul(A_rank,data)
#    print(tmp[0])
##        cicle+=1
#    res=np.hstack(tmp)
    res=comm.gather(tmp,root=rank)
    print(res[0])
#    result=comm.gather(res,root=0)
#    t2=MPI.Wtime()
#    print('the time is',t2-t1)
            
        
    
        
        
        