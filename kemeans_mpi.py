# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:52:52 2019

@author: yifan
"""

import csv, time, random, math

from mpi4py import MPI

import numpy


def eucl_distance(point_one, point_two):#计算两点欧式距离
    if(len(point_one) != len(point_two)):
        raise Exception("Error: non comparable points")
    
    sum_diff=0
    for i in range(len(point_one)):
        diff = pow((float(point_one[i]) - float(point_two[i])), 2)
        sum_diff += diff
    final = math.sqrt(sum_diff)
    return final


def compare_center(initial_center, derived_center, dimensions, num_clusters, cutoff):
    if(len(initial_center) != len(derived_center)):
        raise Exception("Error: non comparable points")
    flag = 0
    for i in range(num_clusters):
        diff = eucl_distance(initial_center[i], derived_center[i])
        if(diff < cutoff):
            flag += 1
    return flag

nums=10*6

data=[[float((i+1000)/nums),float((2000+i)/nums)] for i in range(nums)]

#data=[]
#with open('kmeans_1.txt','r') as f:
#    for line in f:
#        tmps=line.strip('\n').split()
#        if tmps!=[]:
#            data.append([float(tmp) for tmp in tmps])

def main():
    global data
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    
    dimensions=2
    num_clusters=size
    cutoff = 0.002
    compare_val = 0
    num_points = len(data)
    dimensions = len(data[0])
    initial = []
    for i in range(size):#initial包含所有data
        initial.append(data[i])
    start_time = time.time()
    while True:	
        dist = []
        min_dist = numpy.zeros(num_points)
        for point in data:#dist记录每个rank到其他点的欧式距离
            dist.append(eucl_distance(initial[rank], point))
        temp_dist = numpy.array(dist)
        comm.Reduce(temp_dist, min_dist, op = MPI.MIN)#min_dist记录每个点到每个center最小距离
        comm.Barrier()
        if rank == 0:
            min_dist = min_dist.tolist()#numpy数据类型变list
        recv_min_dist = comm.bcast(min_dist, root = 0)
        comm.Barrier()
        cluster = []
        for i in range(len(recv_min_dist)):
            if recv_min_dist[i] == dist[i]:
                cluster.append(data[i])#表示该点到center的距离就是最小的
        center = []
        center_val = [0] * dimensions
        for i in cluster:
            for j in range(dimensions):
                center_val[j] += float(i[j])
        for j in range(dimensions):
            if(len(cluster) != 0):
                center_val[j] = center_val[j] / len(cluster)#即每个center_val的中心坐标
        center = comm.gather(center_val, root = 0)
        comm.Barrier()
        if rank == 0:
            compare_val = compare_center(initial, center, dimensions, size, cutoff)
            if compare_val == size:
                print('my rank is %d'% rank,center)
                print("Execution time %s seconds" % (time.time() - start_time))
        break_val = comm.bcast(compare_val, root = 0)
        initial = comm.bcast(center, root = 0)
        comm.Barrier()
        if break_val == size:
            break
    MPI.Finalize()
if __name__ == "__main__":
    main()