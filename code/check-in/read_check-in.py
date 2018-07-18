# coding=utf-8
# N表示网络的规模
import re
N = 2
def read_file_checkin():
    file = open("C:\\Users\\Administrator\\Desktop\\a.txt")
    # b是存储签到记录的二维列表，行号表示用户ID，c是过渡列表，用来处理读入的每个data[i]
    data = [];
    b = [];
    c = [];
    for line in file.readlines():
        data.append(line.strip())
    file.close()

    for row in range(N):
        b.append([])

    for i in range(len(data)):
        c = re.split('\t', data[i])
        #去除l标志为00000000000000000000000000000000的记录（无效的记录）
        if(c[4] != '00000000000000000000000000000000'):
            b[int(c[0])].append(c[2])
            b[int(c[0])].append(c[3])

    return b

b = read_file_checkin();
print b