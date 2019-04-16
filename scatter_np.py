# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 22:13:41 2019

@author: yifan
"""

from mpi4py import MPI
import numpy as np
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
if rank == 0:
    array_to_share = np.resize(np.array([1, 2, 3, 4 ,5 ,6 ,7, 8 ,9 ,10]),(3,3))
else:
    array_to_share = None
recvbuf = comm.scatter(array_to_share, root=0)
print("process = %d" %rank ,recvbuf)