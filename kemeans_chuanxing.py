# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:09:33 2019

@author: yifan
"""
import math
import time

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
#print(data)
if __name__=='__main__':
    t1=time.time()
    nums=10*6
    data=[[float((i+1000)/nums),float((2000+i)/nums)] for i in range(nums)]
#    data=[]
#    with open('kmeans_1.txt','r') as f:
#        for line in f:
#            tmps=line.strip('\n').split()
#            if tmps!=[]:
#                data.append([float(tmp) for tmp in tmps])
    cutoff=0.0002
    dimensions=2
    num_clusters=10
    init=[data[i] for i in range(num_clusters)]
#    dists=[[] for i in range(num_clusters)]
#    for point in data:
#        for i in range(num_clusters):
#            dists[i].append(eucl_distance(point,init[i]))
#    clusters=[[] for i in range(num_clusters)]
#    init=[data[i] for i in range(3)]
    count=0
    while True:
        dists=[[] for i in range(num_clusters)]
        clusters=[[] for i in range(num_clusters)]
        min_dis=[]
        for point in data:
            for i in range(num_clusters):
                dists[i].append(eucl_distance(point,init[i]))
        for i in range(len(data)):
            min_dis.append(min([dists[j][i] for j in range(num_clusters)]))
        for i in range(len(data)):
            for j in range(num_clusters):
                if min_dis[i]==dists[j][i]:
                    clusters[j].append(data[i])
        new_center=[[] for k in range(num_clusters)]
        for k in range(num_clusters):
            center_row=sum([clusters[k][j][0] for j in range(len(clusters[k]))])/len(clusters[k])
            center_col=sum([clusters[k][j][1] for j in range(len(clusters[k]))])/len(clusters[k])
            new_center[k]=[center_row,center_col]
        count+=1
        if compare_center(new_center,init,dimensions,num_clusters,cutoff)==num_clusters:
            t2=time.time()
            print(new_center)
            print('the iter times is',count)
            print('the time is:',t2-t1)
            break
        init=[data for data in new_center]
        
          
                
            
            
        