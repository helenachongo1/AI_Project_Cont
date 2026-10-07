# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 13:40:10 2024

@author: Acer
"""
#pip install pandas

#print(pd.__version__)#to check install version
#Pandas[onedimensional(Series,single,column),multidimensional(dataframe,multicolumn)]
'''l1=[2,7,9,3]
data=pd.Series(l1);#every element represents a single row
print(data)#always print with the index value
print(l1)#print elements without index value

data = [1, 2, 3, 4, 5]
series = pd.Series(data)
#print(series)

series2 = series + 10
print(series2)
# Filtering
filtered_series = series[series > 2]
print(filtered_series)
# Statistical Calculations
mean_value = series.mean()
print(mean_value)

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}
df = pd.DataFrame(data)
#print(df)
#print(df[['Name']])
df['Salary'] = [70000, 80000, 90000]
#print(df)

df = df.drop('City', axis=1)
#print(df)
#print(df.loc[[0]])

print(df.loc[[0, 1]])

data = {
  "calories": [420, 380, 390],
  "duration": [50, 40, 45]
}
df = pd.DataFrame(data, index = ["day1", "day2", "day3"])
print(df)

dat = pd.read_csv("C:/Users/Acer/OneDrive/Documents/Python/data.csv")
print(dat)

Biodata = {'Name': ['John', 'Emily', 'Mike', 'Lisa'],
        'Age': [28, 23, 35, 31],
        'Gender': ['M', 'F', 'M', 'F']
        }
df = pd.DataFrame(Biodata)
# Save the dataframe to a CSV file
df.to_csv('Biodata.csv', index=False)

dat = pd.read_csv("C:/Users/Acer/OneDrive/Documents/Python/data.csv")
print(dat.info())
# shows first and last five rows
print(dat.head())
print(dat.tail())
print(dat.describe())

data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago'],
    'Number':[1,2,3]
}
dat = pd.DataFrame(data)
print(dat[['Name']])
print(dat[['Name','Number']])
print(dat.loc[[1]])

import numpy as np
data = {
    'A': [np.nan, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'B': np.random.normal(50, 15, 10),
    'C': np.random.rand(10) * 100,
    'D': np.linspace(1, 10, 10),
    'E': np.logspace(1, 2, 10)
}
df = pd.DataFrame(data)
print(df)

data=[2,7,9,5]
series1=pd.Series(data)
data1=[1,6,4,8]
series2=pd.Series(data1)
serie3=series1+series2
print(serie3)

import numpy as np
list1=[1,2,4,7,8,9,5]

data = {1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G'
}

arr=np.array(['P','R','O','G','R','A','M','M','I','N','G'])
serie0=pd.Series(list1)
serie1=pd.Series(data)
serie2=pd.Series(arr)
print(serie0)
print(serie1)
print(serie2)'''

import pandas as pd
S1=pd.Series(range(6))
S2=pd.Series(['P','Y','T','H','O','N'])
df = pd.concat([S1, S2], axis=1)
print(df)







