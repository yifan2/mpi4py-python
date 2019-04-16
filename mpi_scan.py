# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 11:05:46 2019

@author: yifan
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# ------------------------------------------------------------------------------
# scan
send_obj = [2.5, 0.5, 3.5, 1.5][rank]
recv_obj = comm.scan(send_obj)
# scan by SUM:
# rank 0: 2.5
# rank 1: 2.5 + 0.5 = 3.0
# rank 2: 2.5 + 0.5 + 3.5 = 6.5
# rank 3: 2.5 + 0.5 + 3.5 + 1.5 = 8.0
print('scan with SUM: rank %d has %s' % (rank, recv_obj))
recv_obj = comm.scan(send_obj, op=MPI.MAX)
# scan by MAX:
# rank 0: 2.5
# rank 1: max(2.5, 0.5) = 2.5
# rank 2: max(2.5, 0.5, 3.5) = 3.5
# rank 3: max(2.5, 0.5, 3.5, 1.5) = 3.5
print('scan with MAX: rank %d has %s' % (rank, recv_obj))