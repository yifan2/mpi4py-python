# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 18:19:33 2019

@author: yifan
"""

from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.rank
size=comm.size
print("process %d of %d:%s" %(rank,size,'Hello world!'))

#if rank == 0:
#    data = 10000000
#    destination_process = 4
#    comm.send(data,dest=destination_process)
#    print("sending data % s " % data + "to process % d" % destination_process)
#
#if rank == 1:
#    destination_process = 8
#    data = "hello"
#    comm.send(data,dest=destination_process)
#    print("sending data % s :" % data + "to process % d" % destination_process)
#
#if rank == 4:
#   data = comm.recv(source = 0)
#   print("data received is = % s" % data)
#
#if rank == 8:
#   data1 = comm.recv(source = 1)
#   print("data1 received is = % s" % data1)