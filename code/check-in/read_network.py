#ʶ������·��https://blog.csdn.net/qq_37356660/article/details/78242854?locationNum=5&fps=1
# -*- coding: gbk -*
# coding=utf-8
# N��ʾ����Ĺ�ģ
import re
N = 0#�����ģ
degree = []#�洢�ڵ�Ķ�
net = []#������ڽӾ���
# ��������Ĵ�С
dirfile = "E:\��������\DONE\����3\Route views(D)\\network.pairs"
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
#���ڽӱ�洢����
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

