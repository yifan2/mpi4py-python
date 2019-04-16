# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 14:17:54 2019

@author: yifan
"""

from mpi4py import MPI
comm=MPI.COMM_WORLD
rank=comm.rank
b=comm.allgather(rank)
print('my rank is %d,res is' %rank,b)