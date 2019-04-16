# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 17:31:48 2019

@author: yifan
"""

from mpi4py import MPI
import numpy as np
import os

def split_mat(matrix,k,source):#将矩阵进行分组
    res=[]
    tmp=[]
    width=len(matrix)//k
    for i in range(k-1):
        tmp=[row[i*width:(i+1)*width] for row in matrix]
        res.append(tmp)
    res.append([row[(k-1)*width:] for row in matrix])
    return res

#def del_dul(l):
#    res=[]
#    for i in l:
#        if i not in res:
#            res.append(i)
#    return res

if __name__=='__main__':
    source=0
    adj_matrix = [[0, 2, 1, 4, 5, 1],
                  [1, 0, 4, 2, 3, 4],
                  [2, 1, 0, 1, 2, 4],
                  [3, 5, 2, 0, 3, 3],
                  [2, 4, 3, 4, 0, 1],
                  [3, 4, 7, 3, 1, 0]]
#    a=split_mat(adj_matrix,2,0)
    seen=[source]
    dist=adj_matrix[source]
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    print('my rank is',rank)
    m=len(adj_matrix)
    if rank==0:
        split_mat=split_mat(adj_matrix,size,source)
    else:
        split_mat=None
    mat=comm.scatter(split_mat,root=0)
    if rank==0:
        final=[1]+[0]*(m//size-1)
    elif 1<=rank<size-1:
        final=[0]*(m//size)
    else:
        final=[0]*(m-(size-1)*m//size)
#    print(final)
    t1=MPI.Wtime()
    while True:
        min=float('inf')
        for i in seen:
            for j in range(len(final)):
                tmp=dist[i]+mat[i][j]
                if dist[i]+mat[i][j]<min and final[j]==0:
                    min=dist[i]+mat[i][j]
                    local=rank*(m//size)+j
                    p=j
#        if min==float('inf'): #有可能某个rank的所有final都为1
#            print('our result is',dist)
#            print('the time is',MPI.Wtime()-t1)
#            break
        tmp=[min,local,p,rank]#min表示该rank局部最小点，local表示在全局的位置，p表示其在该rank的位置
        tmps=comm.allgather(tmp)
        comm.Barrier()
        tmps=sorted(tmps,key=lambda d:d[0])
        value=tmps[0][0]
        dist_local=tmps[0][1]
        final_local=tmps[0][2]
        rank_local=tmps[0][3]
        if rank==rank_local:
            dist[dist_local]=value
            final[final_local]=1
            seen.append(dist_local)
#            seen=del_dul(seen)
#            print('the seen,final,dist is ',seen,final,dist)
        seen=comm.bcast(seen,root=rank_local)
        dist=comm.bcast(dist,root=rank_local)
        comm.barrier()
        if len(seen)==m:
            print('the time is',MPI.Wtime()-t1)
            print('our result is',dist,seen)
            break     
        
    