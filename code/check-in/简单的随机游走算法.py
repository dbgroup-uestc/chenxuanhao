from numpy import *
import numpy as np

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