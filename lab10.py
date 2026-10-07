# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 20:44:46 2024

@author: Acer
"""

# data to display on plots 
'''x = [3, 1, 3] 
y = [3, 2, 1] 
plt.plot(x, y)
plt.title("Line Chart")
# Adding the legends
plt.legend(["Line"])
plt.show()

import numpy as np 
x = np.linspace(0.1, 2 * np.pi, 41) 
y = np.exp(np.sin(x)) 
plt.stem(x, y) 
plt.show() 

x = [3, 1, 3, 12, 2, 4, 4] 
y = [3, 2, 1, 4, 5, 6, 7] 

# This will plot a simple bar chart
plt.bar(x, y)
# Title to the plot
plt.title("Bar Chart")
# Adding the legends
plt.legend(["bar"])
plt.show()

x = [1, 2, 3, 4, 5, 6, 7, 4] 
# This will plot a simple histogram
plt.hist(x, bins = [1, 2, 3, 4, 5, 6, 7])
# Title to the plot
plt.title("Histogram")
# Adding the legends
plt.legend(["bar"])
plt.show()

x = [3, 1, 3, 12, 2, 4, 4]
y = [3, 2, 1, 4, 5, 6, 7]
# This will plot a simple scatter chart
plt.scatter(x, y)
# Adding legend to the plot
plt.legend("A")
# Title to the plot
plt.title("Scatter chart")
plt.show()

import numpy as np
# Creating dataset
np.random.seed(10)
data = np.random.normal(100, 20, 200)
fig = plt.figure(figsize =(10, 7))
# Creating plot
plt.boxplot(data)

# show plot
plt.show()

x = [1, 2, 3, 4] 
# this will explode the 1st wedge
# i.e. will separate the 1st wedge
# from the chart
e  =(0.1, 0, 0, 0)
# This will plot a simple pie chart
plt.pie(x, explode = e)
# Title to the plot
plt.title("Pie chart")
plt.show()

# making a simple plot
x =[1, 2, 3, 4, 5, 6, 7]
y =[1, 2, 1, 2, 1, 2, 1]
# creating error
y_error = 0.2
# plotting graph
plt.plot(x, y)
plt.errorbar(x, y,yerr = y_error,fmt ='o')

x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]
z = [1, 8, 27, 64, 125]
# Creating the figure object
fig = plt.figure()
# keeping the projection = 3d
# creates the 3d plot
ax = plt.axes(projection = '3d')
ax.plot3D(z, y, x)

import numpy as np
a=int(input("Enter the magnitude value:"))
#f=int(input("Enter the frequency value:"))
t=np.arange(0,10);
y=a*np.sin(2*np.pi*0.1*t)
plt.plot(t,y)
plt.show()

Programminglanguages=['Java', 'Python', 'PHP', 'JavaScript', 'C#', 'C++']
Popularity=[ 22.2, 17.6, 8.8, 8, 7.7, 6.7]
plt.bar(Programminglanguages,Popularity)
plt.title("Popularity of programming languages")
plt.show()


a=int(input("Enter the magnitude value:"))
t=np.arange(0,10);
y=a*np.cos(2*np.pi*0.1*t)
plt.plot(t,y)
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Cos function graph')
plt.show()'''

import matplotlib.pyplot as plt 
import numpy as np

'''x=np.arange(0,10)
y=x**2
plt.plot(x,y, label='Line 1')
x1=np.arange(0,10)
y1=x/2
plt.plot(x1,y1,label='Line 2')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title("Two lines at same graph")
plt.legend()
plt.show()'''
X = np.arange(1, 50)
Y = [value * 3 for value in X]
plt.plot(X, Y)
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('Draw a line.')
print(plt.axis()) 
plt.axis([0, 100, 0, 200]) 
plt.show()




