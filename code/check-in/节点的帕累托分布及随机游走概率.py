# coding=utf-8
#读取处理签到位置后的数据，并求每个节点的稳态pagerank分布

from numpy import *
import numpy as np
import re
from itertools import chain#将二维列表转换成一维列表
from math import sin, asin, cos, radians, fabs, sqrt

EARTH_RADIUS = 6371  #地球平均半径，6371km
N = 58228

def hav(theta):
    s = sin(theta / 2)
    return s * s


def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance#km

file = open("C:\\Users\\Client\\Desktop\\check_ins.txt")

data = []
b = []
for line in file.readlines():
    data.append(line.strip())
file.close()

for row in range(N):
    b.append([])

for i in range(len(data)):
    c = re.split('\t', data[i])
    # 去除l标志为00000000000000000000000000000000的记录（无效的记录）并保证是正确的数据
    b[int(c[0])].append(c[0])
    b[int(c[0])].append(c[1])
    b[int(c[0])].append(c[2])
    b[int(c[0])].append(c[3])
    b[int(c[0])].append(c[4])

#print(b)

prlist = []*N#存储用户的稳态pagerank分布（三维列表）如['0', [[0.3877791559007403], [0.21481875829267286], [0.3974020858065864]], '1', [[0.35086500807316184], [0.6491349919268378]], '2', [[1.0]], '3', [[0.6491349919268378], [0.35086500807316184]]]
pareto = [999.0]*N#存储节点的帕累托分布参数alpha（初始化没有签到记录以及全在同一个地点签到的用户的alpha为999（无效的记录））


#print(prlist)
for i in b:
    c = i#节点的按时间排序的签到记录，如['0', '20101016034854', '39.891077', ' -105.068532', ' 0', '0', '20101016034856', '39.747652', ' -104.99251', ' 1', '0', '20101016035856', '39.891383', ' -105.070814', ' 2', '0', '20101016060204', '39.891077', ' -105.068532', ' 0', '0', '20101017014853', '39.891383', ' -105.070814', ' 2']
    if(c == []):
        continue
    #print('c',c)
    lenmat = 0
    #print(len(c))
    # 求最大的位置标号方便建立N*N的Google矩阵
    for i in range(0, len(c), 5):
        if (lenmat < int(c[i + 4])):
            lenmat = int(c[i + 4])
    #print(lenmat)
    #print(len(c))

    A = np.mat(zeros((lenmat + 1, lenmat + 1)))
    # 建立google矩阵
    for i in range(4, len(c) - 5, 5):
        #print(i,i+5)
        if (int(c[i]) == int(c[i + 5])):  # 如何当前用户没有改变位置（产生自环），则进行下一次循环
            continue
        else:
            #print(i, i + 5)
            A[int(c[i]), int(c[i + 5])] = 1  # 注意矩阵赋值和数组赋值的不同，数组是[][]
            # print(i, i + 5)
    #print(A)

    count = A.sum(axis=1)  # 得到矩阵每一行的和，返回一个N*1的矩阵axis=0代表返回的是列的和(1*N)https://blog.csdn.net/Sunshine_in_Moon/article/details/50278723
    # print(count)
    # 将google矩阵的每一行进行归一化
    for i in range(A.shape[0]):  # m.shape[0]代表的是矩阵的行数,shape[1]代表矩阵的列数https://blog.csdn.net/taoyanqi8932/article/details/52703686
        if (count[i] == 0):
            A[i, :] = 1 / A.shape[1]  # 如果当前节点是悬挂节点（该行为0），则要先进行修正，将其所在行所有值赋为1/N（随机指向网络中的其他节点）
        else:
            A[i, :] = A[i, :] / count[i]

    #print(A)
    # 创建PR转置矩阵(N*1)
    PR = np.mat(ones(A.shape[0]))
    # print(PR)
    # 对PR转置矩阵(N*1)进行归一化
    PR = PR / PR.sum(axis=1)
    # print(PR)
    PR = PR.T
    # print(PR)
    s = 0.15  # 重启概率
    restart = np.mat(ones((A.shape[0], A.shape[0])))  # 创建重启矩阵(元素全为1的N*N矩阵)
    # print(restart)
    A1 = (1 - s) * A + s / A.shape[0] * restart  # matrix(N*N)
    # print(A)
    # print(A1)
    A1 = A1.T
    # print(A1)
    A2 = A1
    # 进行循环以得到收敛的矩阵
    for i in range(1000):
        temp = A2
        A2 = A2 * A1
        if (abs(temp - A2).sum() < 0.001):  # 如果本次迭代和下次迭代得到的矩阵所有元素的总和小于0.001，则认为已经收敛
            break

    prnode = A2 * PR  # node节点的稳态概率(matrix)[[0.21481876]，[0.38777916]，[0.39740209]]

    #print('prnode',prnode)
    prlist.append(c[0])
    prlist.append(prnode.tolist())#存储用户的稳态pagerank分布（三维列表）tolist()方法是把matrix转换成二维列表如matrix([[1, 2, 3]])转换成list[[1, 2, 3]]
    #print('prlist', prlist)
    '''
    求节点的帕累托分布参数alpha
    '''
    n = len(c)/5#用户的签到次数
    #print(n)
    sum = 0.0
    for i in range(0,len(c)-5,5):
        lat1 = float(c[i+2])
        lon1 = float(c[i+3])
        lat2 = float(c[i+7])
        lon2 = float(c[i+8])
        dis = get_distance_hav(lat1, lon1, lat2, lon2)#km
        #print(dis)
        sum += math.log(dis+1)
        #print()
    #print(sum)

    if (sum == 0.0):  # 如果用户的签到记录全部都是在一个点，则令其alpha=999.0（无效的记录）
        pareto[int(c[i])] = (999.0)
    else:
        # print(sum)
        pareto[int(c[0])] = (n - 1) / sum


#print('prlist',prlist)#['0', [[0.3877791559007403], [0.21481875829267286], [0.3974020858065864]], '1', [[0.35086500807316184], [0.6491349919268378]], '2', [[1.0]], '3', [[0.6491349919268378], [0.35086500807316184]]]
#print('1111',prlist[6])
#print(len(prlist))

nodeprlist = []#存储用户稳态pagerank的二维列表[0, [0.3877791559007403, 0.21481875829267286, 0.3974020858065864], 1, [0.35086500807316184, 0.6491349919268378], 2, [1.0], 3, [0.6491349919268378, 0.35086500807316184]]


#print(prlist)
for i in range(0,len(prlist),2):
    #print(prlist[i],prlist[i+1])0 [[0.3877791559007403], [0.21481875829267286], [0.3974020858065864]]
    j = int(prlist[i])  # 当前节点号
    pr1 = prlist[i+1]#例如prl：[[0.21481875829267286], [0.3877791559007403], [0.3974020858065864]]
    a = list(chain.from_iterable(pr1))#将二维列表转换为一维列表[0.21481875829267286, 0.3877791559007403, 0.3974020858065864]依次为列表c中的第0,1,2号位置的稳态分布
    nodeprlist.append(j)
    nodeprlist.append(a)

#print('nodeprlist',nodeprlist)#[0, [0.3877791559007403, 0.21481875829267286, 0.3974020858065864], 1, [0.35086500807316184, 0.6491349919268378], 2, [1.0], 3, [0.6491349919268378, 0.35086500807316184]],nodeprlist[i][j]表示i节点在j位置的概率
#print(pareto)#[0.6481468492593434, 0.6402534241568145, 999.0, 0.5925151963778462]下标为节点号，值为节点的帕累托参数alpha

file = open("C:\\Users\\Client\\Desktop\\results.txt",'w+')

for i in b:
    c = i
    if(c == []):
        continue
    else:
        #print('c',c)
        l1 = nodeprlist.index(int(c[0]))#找到当前节点号在nodeprlist中的索引
        #print('index',nodeprlist.index(int(c[0])))
        for k in range(len(nodeprlist[l1+1])):#当前节点的pagerank概率分布[0.21481875829267286, 0.3877791559007403, 0.3974020858065864]
            h = 4
            while(h<len(c)):
                if(int(c[h]) == k):
                    file.write(c[0] + '\t' + str(pareto[int(c[0])]) + '\t' + str(c[h - 2]) + '\t' + str(c[h - 1]) + '\t' + str(nodeprlist[l1 + 1][k]) + '\n')
                    break
                h += 5

file.close()
#检查一下求节点的帕累托分布参数alpha，利用地图在算算看看距离是否求正确
