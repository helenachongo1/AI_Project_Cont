# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 13:40:47 2024

@author: Acer
"""

'''import numpy as np
y=np.random.rand(5) #Only positive numbers will be printed 
x=np.random.randn(5) #Both positive and negative values will be printed
#print(y)
#print(x)
z=np.random.randint(2,5,5,dtype="int32") #Here only values of integer datatype will be
#printed, each for 4bytes,starting from 2 to 5-1, and 5 values
#print(z)'''

import numpy as np
l1=np.array([[3,2],[4,5]])
arr=np.array([[1,2],[4,6]])
print(np.dot(l1,arr))
print(np.matmul(l1,arr))
print((l1@arr).T) #.T is used to transpose the matrix // np.transpose
print(np.linalg.det(arr))

#lab8
'''import example as addition
a = addition.add(4,5)
print(a)

#import standard math module 
import math
# use math.pi to get value of pi
print("The value of pi is", math.pi)

# import module by renaming it
import math as m
print(m.pi)

# import only pi from math module
from math import pi
print(pi)

# import all names from the standard module math
from math import *
print("The value of pi is", pi)

import math
#print(dir(math))
help('modules')

import math as m
r=int(input("Enter the value of radius:"))
a=m.pi*(r**2)
print("The area of circle: ",a)

import math 
print (math.inf) 
print (-math.inf)

#print(m.cos(2*m.pi))
#Exercise a
import math as m 
x=int(input("Enter the angle in degree: "))
y=x*(m.pi/180)
print("The angle in radian: ",y)

#Exercise b
import math as m
x=int(input("x: "))
y=6*(x**2)+4*(m.sin(x))
print("y= ",y)'''

#Exercise c
'''import math as m
y1=m.cos(2*m.pi)
y2=(-2)*m.sin(2*m.pi)
y3=(-4)*m.cos(2*m.pi)
print("f(x) = ",y1)
print("f'(x) = ",y2)
print("f''(x) = ",y3)'''




