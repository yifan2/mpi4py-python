# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 15:15:52 2019

@author: yifan
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# reduce generic object from each process to root by using reduce
if rank == 0:
    send_obj = 0.5
elif rank == 1:
    send_obj = 2.5
elif rank == 2:
    send_obj = 3.5
else:
    send_obj = 1.5

## reduce by SUM: 0.5 + 2.5 + 3.5 + 1.5 = 8.0
#recv_obj = comm.reduce(send_obj, op=MPI.SUM, root=1)
#print 'reduce by SUM: rank %d has %s' % (rank, recv_obj)
## reduce by MAX: max(0.5, 2.5, 3.5, 1.5) = 3.5
#recv_obj = comm.reduce(send_obj, op=MPI.MAX, root=2)
#print 'reduce by MAX: rank %d has %s' % (rank, recv_obj)


# ------------------------------------------------------------------------------
# reduce numpy arrays from each process to root by using Reduce
send_buf = np.array([0, 1], dtype='i') + 2 * rank
if rank == 2:
#    recv_buf = np.ones(2, dtype='i')
    recv_buf=np.array([4,5])
else:
    recv_buf = None

# Reduce by SUM: [0, 1] + [2, 3] + [4, 5] + [6, 7] = [12, 16]
comm.Reduce(send_buf, recv_buf, op=MPI.MIN, root=2)#recv_buf的数据会被替换掉
print('Reduce by SUM: rank %d has %s' % (rank, recv_buf))

