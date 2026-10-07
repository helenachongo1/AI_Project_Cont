'''#Find common element 
t1=(4,7,6,4,8,9)
t2=(5,8,4,0,2,1)
c=tuple(set(t1)&set(t2))
print(c)


tuple1=(2,3,6,8,4)
print(type(tuple1))
print(tuple1)


numbers = (1, 2, -5)
print(numbers)

a_tuple = (0, [1, 2, 3], (4, 5, 6), 7.0)
print(a_tuple)

languages = ('Python', 'Swift', 'C++')
# access the first item
print(languages[0])   # Python

cars = ('BMW', 'Tesla', 'Ford', 'Toyota')
print('Total Items:', len(cars))

a = tuple(range(5))

b = tuple(range(5,10))
print(b)

c = tuple(range(0,10,2))
print(c)

d = tuple(range(10,0,-2))
print(d)

d = (3,[5,6,7],(4,5,6),[5,6,7,(6,7,8)],9,10)
#Extract 6
print(d[1][1])
print(d[2][2])

t1 = (2,3,4,5)
print(sum(t1))

t3 = (3,4,4,2,2,3,6,7,4,4)
print(t3.count(4))
#print(t3.count(4,2))

t3 = (3,4,4,2,2,3,6,7,4,4)
print(t3.index(2))
print(t3.index(4,3,9))

t3 = (3,4,4,2,2,3,6,7,4,4)
print(min(t3))

numbers = (7, 2, 8, 5, 9)
print(max(numbers))'''

'''a = (5,6,7,5,5,9,7)
b = ("a","b","v","b")
my_tu_1 = tuple(dict.fromkeys(a))
print(my_tu_1)
my_tu_2 = tuple(dict.fromkeys(b))
print(my_tu_2)

first_names = ('Simon', 'Sarah', 'Mehdi', 'Fatime')
last_names = ('Sinek', 'Smith', 'Lotfinejad', 'Lopes')
ages = (49, 55, 39, 33)
zipped = tuple(zip(first_names, last_names,ages))
print(zipped)

b = ((1,2),(3,4),(5,6))
my = tuple(item for l in b for item in l)
print(my)

#Exrecise d
a=(3,2,5,6,7,0,12,3,4,6,2,13)
print("Maximum element:",max(a))
print("Minimum element:",min(a))
#Exercise e
b=('P','y','t','h','o','n')
c="".join(b)
print(c)
for i in b:
    print(i, end="")'''
    
#Exercise f
c=(34,65,12,7,89,57,43,2,5)
print("The original tuple:",c)
print("The sorted tuple:",sorted(c))
#print(c.sort())

'''#Exercise g
c=(34,65,12,7,89,57,43,2,5)
print("The first element is:",c[0])
print("The last element is:",c[-1])

#Exercise b
c=(34,65,12,7,89,57,43,2,5)
b=False
n=8
for i in c:
    if n==i:
        b=True
        print(n,"exists in c")
        break
    else:
        print(n,"does not exist in c")
        break
#Exercise c
c=('P','y','t','h','o','n',' ','5')
str1=" "
for i in c:
    str1=str1+i
print(str1)

#Exercise a
c=(34,65,12,7,89,57,43,2,5,12,65,2,7)
print("The occurence of element 7 is:",c.count(7))

a = tuple(range(5))
print(a)'''













