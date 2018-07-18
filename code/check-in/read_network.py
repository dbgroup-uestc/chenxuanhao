#识别中文路径https://blog.csdn.net/qq_37356660/article/details/78242854?locationNum=5&fps=1
# -*- coding: gbk -*
# coding=utf-8
# N表示网络的规模
import re
N = 0#网络规模
degree = []#存储节点的度
net = []#网络的邻接矩阵
# 计算网络的大小
dirfile = "E:\无向网络\DONE\网络3\Route views(D)\\network.pairs"
def networksize():
   file = open(dirfile)
   n = 0
   for line in file:
       (id1,id2) = line.split()
       n1 = max(int(id1),int(id2))
       if(n1 > n):
           n = n1
   file.close()
   return n

N = int(networksize()) + 1
print(N)
#以邻接表存储网络
def read_network():
    n = []
    global degree
    degree = [0]*N
    for row in range(N):
        n.append([])
    file = open(dirfile)
    for line in file:
        (id1, id2) = line.split()
        n[int(id1)].append(id2)
        degree[int(id1)] += 1
    return n

net = read_network()
'''
print net[2123]
count = 0
for i in degree:
    count += i
print count/2
'''

