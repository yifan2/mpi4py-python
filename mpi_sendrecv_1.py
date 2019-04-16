# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 23:09:37 2019

@author: yifan
"""

from mpi4py import MPI

comm=MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

nxt = (rank+1)%size
prev = (rank-1)%size

num = rank

num2 = comm.sendrecv(num,dest=nxt,source=prev)

print(rank, num2)