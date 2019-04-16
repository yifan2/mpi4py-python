# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 23:04:08 2019

@author: yifan
"""

import numpy as np
from mpi4py import MPI


comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# create a 3 x 2 Cartesian topocomm
#      period = True  period = True
#       |   (4)     |   (5)     |
# ------+-----------+-----------+--------
# (-2)  |  0,0 (0)  |  0,1 (1)  |  (-2)     period = False
# ------+-----------+-----------+--------
# (-2)  |  1,0 (2)  |  1,1 (3)  |  (-2)     period = False
# ------+-----------+-----------+--------
# (-2)  |  2,0 (4)  |  2,1 (5)  |  (-2)     period = False
# ------+-----------+-----------+--------
#       |   (0)     |   (1)     |
dims = [3, 2]
periods = [True, True]
cart_comm = comm.Create_cart(dims, periods)
#print('rank %d has topo:' % rank, cart_comm.topo
#print('rank %d has coords:' % rank, cart_comm.coords)
#print('rank %d has dims:' % rank, cart_comm.dim)
#print 'rank %d has periods:' % rank, cart_comm.periods

#print('rank 3 has coords:', cart_comm.Get_coords(3))
#print('coords [1, 1] is rank:', cart_comm.Get_cart_rank([1, 1]))

# shift
sd = cart_comm.Shift(0, 1)#表示该rank上下的点
print('shift hhh for row: rank %d has (source, dest)=(%d,%d)' %(rank,sd[0],sd[1]))#表示该rank左右的点
sd = cart_comm.Shift(1, 1)
print('shift 233 for column: rank %d has (source, dest) = (%d, %d)' %(rank, sd[0], sd[1]))
