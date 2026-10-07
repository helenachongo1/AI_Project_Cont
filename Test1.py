# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 13:43:05 2024

@author: Acer
"""

#Test
#1. 
'''l2=[25,36];
s1=l2[0]%10
s2=l2[1]%10
sum=s1+s2
print(sum)'''

#2.
'''list1=[2,5,7,4,9,3]
for i in range(0,6):
    if list1[i]%2==0:
        list2=list1[i]
        print("even:",list2)
    else:
        list3=list1[i]
        print("odd:",list3)'''
        

#3
'''a=int(input("Value of a:"))
b=int(input("Value of b:"))
try:
    c=a/b
    print(c)
except ZeroDivisionError:
    print("Not possible")'''
    
#4

'''def maxi(a,b,c):
    if(a>b):
        if(a>c):
            print("Maximum:",a)
    elif (b>c):
        print("Maximum:",b)
    else:
        print("Maximum:",c)

        
a=int(input("Value of a:"))
b=int(input("Value of b:"))
c=int(input("Value of c:"))
s=maxi(a,b,c)
print(s)'''

#7
'''list1=[12,23]
s1=list1[0]%10
s2=list1[1]%10
p=s1*s2
print("The product:",p)'''

#8
'''import numpy as np
a=np.array([[0,1,2],
           [3,4,5],
           [6,7,8]])
reve=a[:,::-1]
print(reve)'''

#9
'''import numpy as np
import matplotlib.pyplot as plt 

a=int(input("Enter the amplitude:"))
t=np.arange(0,10)
y=a*np.sin(2*np.pi*(0.1)*t)
plt.plot(t,y)
plt.xlabel("x-axis")
plt.ylabel("y-axis")
print(plt.axis())
plt.show()'''

#10
'''import numpy as np
import matplotlib.pyplot as plt 

a=int(input("Enter the amplitude:"))
t=np.arange(0,10)
y=a*np.sin(2*np.pi*(0.035)*t)
plt.plot(t,y)
plt.show()'''

#1.1
'''a=0
for i in range(1,6):
    while(a<i):
        if i%2==0:
            print(i*"#")
        else:
            print(i*"*")
        a=a+1 
    print(" ")'''
    
#6
'''list1=[1,2,5,10,11,14,17,20]
res = list(set(range(max(list1) + 1)) - set(list1))
print("The missing values:")
print(res)'''
    
import numpy as np

a = np.array([2, 6, 1, 9, 10, 3, 27])

min_val = 5
max_val = 11

mask = (a >= min_val) & (a <= max_val)

result = a[mask]

print("Numbers in the range", min_val, "to", max_val, ":", result)
        



