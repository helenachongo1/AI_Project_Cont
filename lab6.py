# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 13:45:57 2024

@author: Acer
"""

'''x = 10
if x>5:
    print("x is greater than 5")

x = 10
if  x>5:
    print("x is greater than 5")
elif x ==5:
   print("x is equal to 5")
else:
   print("x is less than 5")

x = 10   
if x>5:
   print("x is greater than 5")
else:
   print("x is not greater than 5")
   
age = 35

if age >= 60:
    print("You are a senior citizen.")
else:
    if age >= 18:
        print("You are an adult.")
    else:
        print("You are a teenager.")
        
num = 10

if num > 0:
    if num % 2 == 0:
        print("The number is positive and even.")
    else:
        print("The number is positive but odd.")
else:
    print("The number is not positive.")
    
Fruits = ["apple", "banana", "cherry"]
for fruit in Fruits:
      print(fruit)
      
x = 1
while x<=5:
     print(x)
     x+=1
     
for x in range(1,6):
    if x==3:
        break
    print(x)
    
for x in range(1,6):
    if x==3:
        continue
    print(x)
    
for x in range(1,6):
    if x == 3:
        pass
    print(x)
    
my_list = [1, 2, 3, 4, 5]
print(len(my_list))

def add_numbers(a, b):
    return a + b
result = add_numbers(3, 5)
print(result)

add = lambda x, y: x + y
print(add(3, 5))

def factorial(n):

    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)
print(factorial(5)) 

def square(x):
    return x * x
numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(square, numbers))
print(squared_numbers)

def generate_numbers():
    for i in range(1, 6):
        yield i
for number in generate_numbers():
    print(number)

#Exercise a
x=1
while x<=100:
    if x%2==1 :
        print(x)
    x+=1
    
#Exercise b
n=int(input("Enter the value of n:"))
sum=0
for x in range(1,n):
    sum+=x
print(sum)

#Ex'ercis'e c
'digit=int(input("Enter any digit:"))
count=0
while(digit!=0):
    digit=digit//10
    count+=1
print(count)

#Exercise f
digit=int(input("Enter any digit:"))
p=1
while(digit != 0):
    r=digit%10
    p*=r
    digit=digit//10
print(p)

#Exercise g
digit=int(input("Enter any digit:"))
p=1
while(digit != 0):
    r=digit%10
    print(r,end="")
    digit=digit//10
    
#Exercised

import math
digit=int(input("Enter the number:"))
p=int(math.log10(digit))
lastdigit=digit%10
firstdigit=digit//(10**p)
x=firstdigit*(10**p)
y=digit%x
def swap(y,lastdigit,firstdigit,p):
    num=y//10 
    num=(lastdigit*(10**p))+num*10+firstdigit
    return num

print("After swap first and last digits:",swap(y,lastdigit,firstdigit,p))'''

try:
  number = int(input("Enter a number: "))
  result = 10 / number
  print("The result is:", result)
except ZeroDivisionError:
  print("Division by zero is not allowed.")
except ValueError:
  print("Invalid input. Please enter a valid number.")
















