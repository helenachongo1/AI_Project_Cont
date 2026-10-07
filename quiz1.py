# -*- coding: utf-8 -*-
"""
Created on Fri Jul 25 20:23:14 2025

@author: Acer
"""
'''
for i in range(2,10,2):
    for j in range(1,5):
        print(j, "Loop")
        '''
'''        
count = 0
for i in range(1,5):
    for j in range(1, i+1):
        count+=1
print(count)'''

n = 100
i = 1
while i < n:
    print(i)
    i *= 3