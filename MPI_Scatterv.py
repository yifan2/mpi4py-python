# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 10:26:13 2019

@author: yifan
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# scatter a list of generic object by using scatter
if rank == 1:
    send_obj = [1.2, 'xxx', {'a': 1}, (2,)]
else:
    send_obj = None

# each process receives one of the element of send_obj from rank 1
#     rank 0   |   rank 1   |   rank 2   |   rank 3
#  ------------+------------+------------+------------
#      1.2     |   'xxx'    |  {'a': 1}  |   (2,)
recv_obj = comm.scatter(send_obj, root=1)
print('scatter: rank %d has %s' % (rank, recv_obj))


# ------------------------------------------------------------------------------
# scatter a numpy array by using Scatter
if rank == 2:
    send_buf = np.arange(8, dtype='i')
else:
    send_buf = None
recv_buf = np.empty(2, dtype='i')

# each process receives two numbers of send_buf from rank 2
#     rank 0   |   rank 1   |   rank 2   |   rank 3
#  ------------+------------+------------+------------
#     [0, 1]   |   [2, 3]   |   [4, 5]   |   [6. 7]
comm.Scatter(send_buf, recv_buf, root=2)
print('Scatter: rank %d has %s' % (rank, recv_buf))


# ------------------------------------------------------------------------------
# scatter a numpy array by using Scatter with MPI.IN_PLACE
if rank == 2:
    send_buf = np.arange(8, dtype='i')
else:
    send_buf = None
# initialize a receive buffer [-1, -1]
recv_buf = np.zeros(2, dtype='i') - 1

# each process other than the root receives two numbers of send_buf from rank 2
# but the root does not receive message from itself with MPI.IN_PLACE
#     rank 0   |   rank 1   |   rank 2   |   rank 3
#  ------------+------------+------------+------------
#     [0, 1]   |   [2, 3]   |  [-1, -1]  |   [6. 7]
if rank == 2:
    comm.Scatter(send_buf, MPI.IN_PLACE, root=2)
else:
    comm.Scatter(send_buf, recv_buf, root=2)
print('Scatter: rank %d has %s with MPI.IN_PLACE' % (rank, recv_buf))


# ------------------------------------------------------------------------------
# scatter a numpy array by using Scatterv
if rank == 2:
    send_buf = np.arange(10, 20, dtype='i')
else:
    send_buf = None
recv_buf = np.zeros(rank+1, dtype='i')#用empty会报错
count = [1, 2, 3, 4]
displ = [0, 1, 3, 6]
# scatter 10 numbers from rank 2 to 4 processes with allocation:
#       rank 0   |   rank 1   |   rank 2   |   rank 3
#     -----------+------------+------------+-------------
#         10     |   11 12    |  13 14 15  | 16 17 18 19
# displ:  0          1           3           6
#
comm.Scatterv([send_buf, count, displ, MPI.INT], recv_buf, root=2)
#comm.Scatterv(send_buf,recv_buf,root=2)
print('Scatterv: rank %d has %s' % (rank, recv_buf))