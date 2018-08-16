# coding=utf-8
# N表示网络的规模
#处理原始数据，删除用户的假签数据以及改变签到位置标识0,1,2...
import re
from numpy import *
import numpy as np
import gc
from datetime import datetime
from math import sin, asin, cos, radians, fabs, sqrt

EARTH_RADIUS = 6371  #地球平均半径，6371km
N = 58228
flyspeed = 900.0#民航客机的速度km/hs
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


def read_file_checkin():
    file = open("C:\\Users\\Client\\Desktop\\graph\\Brightkite_totalCheckins.txt")
    # b是存储签到记录的二维列表，行号表示用户ID，c是过渡列表，用来处理读入的每个data[i]
    data = [];
    a = [];
    b = [];
    c = [];
    s = "";
    for line in file.readlines():
        data.append(line.strip())
    file.close()
    #print(data)
    for row in range(N):
        b.append([])

    for i in range(len(data)):
        c = re.split('\t', data[i])
        #去除l标志为00000000000000000000000000000000的记录（无效的记录）并保证是正确的数据
        if(len(c) == 5):
            if(c[4] != '00000000000000000000000000000000' and c[2]!='0.0' and c[3] != '0.0'):
                s = c[1]
                a = re.split('-|T|Z|:', s)
                a.pop()#删除末尾产生的空格
                s = ""
                for i in a:
                    s += i
                b[int(c[0])].append(c[0])
                b[int(c[0])].append(s)
                b[int(c[0])].append(c[2])
                b[int(c[0])].append(c[3])
                b[int(c[0])].append(c[4])

    return b

b = read_file_checkin();
#print(b)

#移除签到记录小于10次的节点
'''
不用for循环的原因：在python中，for循环相当于一个迭代器（Iterator），在循环体中改变循环变量的值对循环次数是没有影响的。 
迭代器在一个独立的线程中工作，并且拥有一个mutex锁。迭代器被创建的时候，建立了一个内存索引表（单链表），这个索引表指向原来的对象，
当原来的对象数量改变的时候，这个索引表的内容没有同步改变，所以当索引指针往下移动的时候，便找不到要迭代的对象，
于是产生错误。就是说迭代器在工作的时候，是不允许被迭代的对象被改变的。
for i in range(10):

　　i=5

此时给i赋值为5的时候并没有改变循环的次数

如果要想该变循环次数的话可以使用while语句
'''
'''
i = 0
while i < len(b):
    if (len(b[i])/5 < 10):
        #print('b[i]',b[i])
        b.remove(b[i])
        i -= 1
    i += 1
#print(b)
'''

#处理数据
fileb = open("C:\\Users\\Client\\Desktop\\check_ins.txt",'w+')

for ch in b:
    a = ch#读取node节点的签到数据
    #print('a',a)

    a1 = []  # 存储节点访问的记录（时间，经度，纬度，位置编码）二维列表
    for i in range(1, len(a), 5):
        a1.append(a[i:i + 4])
    # print('a1',a1)
    a1.sort()  # 以访问时间对节点的签到记录进行排序
    #print('a1',a1)
    #处理假签数据,默认第0次为正确的签到
    i = 0
    while(i<len(a1)-1):
        ch1 = a1[i]#['20081021045549', '49.233804', '-123.116325', 'f016ada49f2311dd9e1c003048c0801e']
        ch2 = a1[i+1]
        t1 = ch1[0]#20081021045549
        year1 = t1[0:4]
        month1 = t1[4:6]
        day1 = t1[6:8]
        hour1 = t1[8:10]
        minute1 = t1[10:12]
        second1 = t1[12:14]
        #2008 - 11 - 21 17: 14:02
        time1 = str(year1) + '-' + str(month1) + '-' + str(day1) + ' ' + str(hour1) + ':' + str(minute1) + ':' + str(second1)
        #print('time1',time1)

        #print(t1)
        t2 = ch2[0]
        year2 = t2[0:4]
        month2 = t2[4:6]
        day2 = t2[6:8]
        hour2 = t2[8:10]
        minute2 = t2[10:12]
        second2 = t2[12:14]
        time2 = str(year2) + '-' + str(month2) + '-' + str(day2) + ' ' + str(hour2) + ':' + str(minute2) + ':' + str(second2)
        #print('time2',time2)

        date1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
        date2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

        deltahours = (date2 - date1).total_seconds()/3600.0#两次签到的间隔小时
        #print('deltahour',deltahours)

        lat1 = float(ch1[1])
        lon1 = float(ch1[2])
        lat2 = float(ch2[1])
        lon2 = float(ch2[2])
        dis = get_distance_hav(lat1, lon1, lat2, lon2)#km
        #print('dis',dis)

        if(dis > deltahours*flyspeed):
            a1.remove(ch2)
            i -= 1
        i += 1

    #print('a1',a1)

    lo = []  # 存储节点访问的所有位置
    for i in a1:
        #print(i)#['20090802064638', '39.220127', '139.900202', '5fc715747f2711de953b003048c0801e']
        lo.append(i[3])
        # print(lo)

    num = set(lo)#以集合形式存储节点的访问位置，排除相同的位置
   # print(num)
    num = list(num)

    dic = {num[i]: i for i in range(len(num))}#建立位置与标号字典，方便建立节点访问位置矩阵，以随机游走求概率分布
    #fileb.write(str(dic)+'\n')
    #print(str(dic))
    #del num
    #gc.collect()#回收num所占的内存



    #将节点的位置编码替换成0,1,....并保存在文件中
    for i in a1:
        #print('i',i)
        i[3] = dic[i[3]]

        fileb.write(str(a[0])+'\t'+str(i[0]) + '\t' + str(i[1]) + '\t' + str(i[2]) + '\t' + str(i[3]) + '\n')


fileb.close()

'''
  sort方法，通过每一行的第一个元素进行排序。对于第一个元素相同的行，
  则通过它们的第二个元素进行排序。如果行中的第一个和第二个元素都相同，
  那么利用他们的第三个元素进行排序，依此类推
'''
'''
a1.sort()
print(a1)

del b
gc.collect()
'''
'''
a = np.mat([[0,0.5,0.5],[0,0,1],[1,0,0]])#matrix
b = np.mat([1/3,1/3,1/3]).T#matrix
c = np.mat(ones((3,3)))#matrix
print(a)
print(b)
print(c)
a1 = 0.85*a+0.15/3*c#matrix
a1 = a1.T
for i in range(10):
    a1 *= a1
b1 = a1 * b
print(b1)
'''
# print(int(b[1][6]) < int(b[1][0]))

'''
s = "2010-10-17T01:48:53Z"
a = re.split('-|T|Z|:',s)
print(a)
a.pop()
print(a)
s = ""
for i in a:
    s += i
print(s)

print(s[2])
'''

'''
a = [[1,2,3,4],[4,5,6],[7,8,9]]
print(len(a))
i = 0
while i<len(a):
    if(len(a[i]) < 4):
        a.remove(a[i])
        i -= 1
    i += 1
print(a)
'''

'''
for i in range(10):

　　i=5

此时给i赋值为5的时候并没有改变循环的次数

如果要想该变循环次数的话可以使用while语句
'''
'''
s1 = "2008-11-21 17:14:02"
s2 = "2008-12-22 18:20:02"
a = datetime.strptime(s1,"%Y-%m-%d %H:%M:%S")
b = datetime.strptime(s2,"%Y-%m-%d %H:%M:%S")
print(a)
print(b)
print((b-a).total_seconds())
'''