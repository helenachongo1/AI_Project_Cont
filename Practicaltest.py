# -*- coding: utf-8 -*-
'''list1=[1,2,3,4,5,6,7,8,9]
for i in list1:
    if i%3==0 & i%5!=0:
        print(list1[i])
        i=i+1'''

'''for i in range(1,100):
    if i%3==0 & i%5!=0:
        print(i)
    
        
List1=[2,56,78,21,2,34,65,56,101,20,102,101]
m_list=list(dict.fromkeys(List1))
print("After removing the duplicates:",m_list)
#my_list_1 = list(dict.fromkeys(my_list_1))'''


'''#1
import numpy as np
arr=np.array([[2,4],[5,8]])
print("The sum of diagonal elements:",np.trace(arr))

#6
List1 = [1, 2, 3]
List2 = [2, 3, 4, 5,6,9]
List1.extend(List2)
print("Before removing duplicates:")
print(List1)
m_list=list(dict.fromkeys(List1))
print("After removing duplicates:")
print(m_list)'''

#2
'''n=100
list1=range(1,n)
for x in list1:
   if x%3==0:
       if x%5!=0:
           list2=list[x]
           print(list2,end=" ")'''

'''req_elements = dict()
res = set()
for i in List1:
    if i in res:
        freq_elements[i] = freq_elements[i] + 1
    else:
        freq_elements[i] = 1
        res.add(i)
print("Frequency of each element is:")
print(freq_elements)'''

m="aabcccccaaa"
n=set()
freq_elements = dict()
for i in m:
    if i in n:
        freq_elements[i]=freq_elements[i]+1
    else:
        freq_elements[i]=1
        n.add(i)
print(freq_elements)

'''dict1={“comp”: “computer” , “sci” : “science”}
print(dict[“comp”])
dict2={“123”:”computer”,456 : “maths”}
print(dict2[“123”])
print(dict1[“comp”]+ dict2[“123”])'''

'''dict1={"math":"Science","Python":"Language"}
dict2={"ese":"25","mooc":"24"}
dict1=dict.fromkeys(dict2)
print(dict1)

b = ((1,2),(3,4),(5,6))
my = tuple(item for l in b for item in l)
print(my)'''


    

