# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 09:56:18 2019

@author: yifan
"""

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.rank
if rank == 0:
    data = {'a': 7, 'b': 3.14}
    print('process %d sends %s' % (rank, data))
    comm.send(data, dest=1, tag=11)
elif rank == 1:
    data = comm.recv(source=0, tag=11)
    print('process %d receives %s' % (rank, data))
