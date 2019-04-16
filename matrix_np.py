# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 22:47:19 2019

@author: yifan
"""


import os, sys, time

import numpy as np

import mpi4py.MPI as MPI

comm = MPI.COMM_WORLD

# the node rank in the whole community

comm_rank = comm.Get_rank()

# the size of the whole community, i.e.,the total number of working nodes in the MPI cluster

comm_size = comm.Get_size()

 

# test MPI

if __name__ == "__main__":

    #create a matrix

   if comm_rank == 0:

       all_data = np.arange(20).reshape(4, 5)
   

    #broadcast the data to all processors

   all_data = comm.bcast(all_data if comm_rank == 0 else None, root = 0)

   

    #divide the data to each processor

   num_samples = all_data.shape[0]

   local_data_offset = np.linspace(0, num_samples, comm_size + 1).astype('int')

   

    #get the local data which will be processed in this processor

   local_data = all_data[local_data_offset[comm_rank] :local_data_offset[comm_rank + 1]]

   print("****** %d/%d processor gets local data ****" %(comm_rank, comm_size))

   print(local_data)

   

    #reduce to get sum of elements

   local_sum = local_data.sum()

   all_sum = comm.reduce(local_sum, root = 0, op = MPI.SUM)

   

    #process in local

   local_result = local_data ** 2

   

    #gather the result from all processors and broadcast it

   result = comm.allgather(local_result)

   result = np.vstack(result)

   

   if comm_rank == 0:

       print("*** sum: ", all_sum)

       print("************ result ******************")

       print(result)
