# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 13:37:20 2024

@author: Acer
"""

"""lab4-create a list"""
'''List1 = [1, 2, 3]
List2 = [2, 3, 4, 5]
# Add List2 to List1
List1.extend(List2)
print(List1)

#list1=[(2,3),6,(1+2j,6),[5,[4,1]],1]
#print(list1[3][1][1])

List = [1, 2, 3, 4, 5]
print(sum(List))

List = ['gfg', 'abc', 3]
print(sum(List))

List = [1, 2, 3, 1, 2, 1, 2, 3, 2, 1]
print(List.count(1))

List = ['a','b','c','d','a']
print(List.count('a'))

List = [1, 2, 3, 1, 2, 1, 2, 3, 2, 1]
print(len(List))

List = [1, 2, 3, 1, 2, 1, 2, 3, 2, 1]
print(List.index(2))

List = [1, 2, 3, 1, 2, 1, 2, 3, 2, 1]
#index value of the element starting from the given intial value
print(List.index(2, 2))

List = [1, 2, 3, 1, 2, 1, 2, 3, 2, 1]
#index value of the element between the given range (from 2 to 7)
print(List.index(2, 5,7))

numbers = [5, 2, 8, 1, 9]
print(min(numbers))

numbers = [5, 2, 8, 1, 9]
print(max(numbers))

List = [2.3,4.445,3,5.33,1.054,2.5]
List.sort()
print(List)

List = [2.3, 4.445, 3, 5.33, 1.054, 2.5]
#Reverse flag is set True
List.sort(reverse=True) 
print(List) 

list = [1,2,3,4,5]
#reversing the list
list.reverse()
#printing the list
print(list)

List = [2.3, 4.445, 3, 5.33, 1.054, 2.5]
print(List.pop())

List = [2.3, 4.445, 3, 5.33, 1.054, 2.5]
print(List.pop(0))

List = [2.3, 4.445, 3, 5.33, 1.054, 2.5]
del List[0]
print(List)

List = [2.3, 4.445, 3, 5.33, 1.054, 2.5]
List.remove(3)
print(List)

my_list_1 = [5, 2, 90, 24, 10, 2, 90, 34]
my_list_2 = ['a', 'a', 'a', 'b', 'c', 'd', 'd', 'e']

# removing duplicates from list 1
#my_list_1 = list(dict.fromkeys(my_list_1))
#print(my_list_1)
my_list_2 = list(dict.fromkeys(my_list_2))
print(my_list_2)

my_list_1 = [5, 2, 90, 24, 10]
my_list_2 = [6, 3, 91, 25, 12]

# combined
my_combined_list = list(zip(my_list_1, my_list_2))
print(my_combined_list)

my_list = ['a', 'a', 'a', 'b', 'c', 'd', 'd', 'e']
most_frequent_value = max(set(my_list), key=my_list.count)
print("The most common element is:", most_frequent_value)

list_of_lists = [[1, 2],
                 [3, 4],
                 [5, 6],
                 [7, 8]]
# using list comprehension
my_list = [item for List in list_of_lists for item in List]
print(my_list)

#exercise 1
list1=[1,2,3,4,5]
p=1
for i in list1:
    p=p*i
    
print(p)

#exercise 2
List=[25,89,45,1,45,76,34,21,23]
print("The largest number of the list is ",max(List))

#exercise 3
List1=[2,56,78,21,2,34,65,56,101,20,102,101]
m_list=list(dict.fromkeys(List1))
print("After removing the duplicates:",m_list)
#my_list_1 = list(dict.fromkeys(my_list_1))

#exercise 4
List1=[2,56,21,2,34,65,56,101,102,101]
print(List1.count(65))
  
freq_elements = dict()
res = set()
for i in List1:
    if i in res:
        freq_elements[i] = freq_elements[i] + 1
    else:
        freq_elements[i] = 1
        res.add(i)
print("Frequency of each element is:")
print(freq_elements)

#exerscise 5
List1=[2,56,21,3,34,65,56,101,102,101]
List2=[3,65,12,2,43,75,36,1011,102,1010]
x1_list=set(List1)
x2_list=set(List2)
if(x1_list & x2_list):
    print(x1_list & x2_list)'''
    
#exercise 6
List1=[3,57,78,21]
for i in List1:
    print(i,end="")







  


















