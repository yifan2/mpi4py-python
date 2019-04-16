# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 18:32:40 2019

@author: yifan
"""

import numpy as np 
from scipy.cluster.vq import kmeans, whiten 
from operator import itemgetter
from math import ceil 
from mpi4py import MPI 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() 
np.random.seed(seed=rank)
# XXX should use parallel RNG 
data=[]
with open('kmeans_1.txt','r') as f:
    for line in f:
        tmps=line.strip('\n').split()
        if tmps!=[]:
            data.append([float(tmp) for tmp in tmps])
K = 10
nstart = 100
n = int(ceil(float(nstart)/size))
centroids, distortion = kmeans(data, K, n)
results = comm.gather((centroids, distortion), root=0)
if rank == 0:
    results.sort(key=itemgetter(1)) 
    result = results[0] 
    print('Best distortion for %d tries: %f' % (nstart,result[1]))
