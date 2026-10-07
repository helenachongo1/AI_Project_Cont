#Q1
#import numpy as np

'''arr=np.array([[1,3,5,7],
              [2,4,7,1],
             [2,4,6,8],
             [7,12,5,9]])

top_row = arr[0, :]
bottom_row = arr[-1, :]
left_column = arr[1:-1, 0]
right_column = arr[1:-1, -1]

border_elm=np.concatenate((top_row, right_column, bottom_row[::-1], left_column[::-1] ))
print("Extracted elements:",border_elm)'''


#Q2
#2.	Write a function that finds the median of each row in a 2D array without using numpy.
#median and sorts rows based on the median values.


'''def median_found(arr):
    med_arr=[]
    for row in arr:
        s_row=sorted(row)
        n=len(s_row)
        m=n//2
        if n% 2 ==0:
            med= (s_row[m-1]+s_row[m])/2
            
        else:
             med=s_row[m]
        med_arr.append((med,row))
        
    med_arr.sort(key=lambda x: x[0])
    new_arr= [row for median, row in med_arr]
    return new_arr

arr=[[1,3,5,7],
    [2,4,7,1],
    [2,4,6,8],
    [7,12,5,9]]

print(median_found(arr))'''

#Q3
#3.	Create a DataFrame with a MultiIndex (using both rows and columns), 
#where row indexes represent countries and cities, and columns represent years and months.
# Write a function that calculates the monthly percentage change in each city’s population

'''import pandas as pd
import numpy as np

arr = [
    ['Mozambique', 'Malysia', 'South Korea', 'India', 'India', 'Thailand', 'Japan', 'China'],
    ['Maputo', 'Kuhala  Lanpur', 'Seoul', 'Mumbai', 'Delhi', 'BangKok', 'Hong Kong', 'Benjing']
]
rows = pd.MultiIndex.from_arrays(arr, names=['Countries', 'Cities'])

columns = pd.MultiIndex.from_tuples(
    [('2022','January'), ('2022','May'),('2022','June'),('2022','October')], names=['Years','Months']
    )

np.random.seed(32)
data=np.random.randint(10000,100000, size=(8,4))

df = pd.DataFrame(data, index=rows, columns=columns)
print(df)

def cal_percentage(df):
    return df.pct_change(axis=1)*100
    
per_c=cal_percentage(df)
print("\nChange in population during a month: ",per_c)'''

import sqlite3

conn = sqlite3.connect('Database_schema.db')
cursor=conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS Products(
                   prod_code TEXT PRIMARY KEY,
                   name TEXT NOT NULL,
                   descript TEXT,
                   price REAL NOT NULL)
               ''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS inventory(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   prod_code TEXT NOT NULL,
                   quant INTEGER NOT NULL,
                   FOREIGN KEY (prod_code) REFERENCES Products (prod_code))
               ''')
               
cursor.execute('''
               CREATE TABLE IF NOT EXISTS Orders(
               order_id INTEGER PRIMARY KEY AUTOINCREMENT,
               prod_code TEXT NOT NULL,
               quant_ordered INTEGER NOT NULL,
               total_price REAL NOT NULL,
               FOREIGN KEY (prod_code) REFERENCES Products (prod_code))
               ''')
               
conn.commit()

def insert_data():
    cursor.execute('''
    INSERT INTO Products (prod_code, name, descript, price) 
    VALUES ('P001', 'Acer lite', 'A high-performance laptop', 1000.00)
    ''')

    cursor.execute('''
    INSERT INTO Products (prod_code, name, descript, price) 
    VALUES ('P002', 'Samsung', 'A feature-packed smartphone', 500.00)
    ''')
    
    cursor.execute('''
    INSERT INTO Inventory (prod_code, quant) 
    VALUES ('P001', 750)
    ''')
    
    cursor.execute('''
    INSERT INTO Inventory (prod_code, quant) 
    VALUES ('P002', 800)
    ''')
    
    cursor.execute('''
    INSERT INTO Orders (prod_code, quant_ordered, total_price) 
    VALUES ('P001', 2, 2000.00)
    ''')
    
    cursor.execute('''
    INSERT INTO Orders (prod_code, quant_ordered, total_price) 
    VALUES ('P002', 3, 1500.00)
    ''')
    
    conn.commit()
    
def display_data():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    print("Products:")
    for p in products:
        print(p)
        
    cursor.execute('SELECT * FROM inventory')
    inventory = cursor.fetchall()
    print("\nInventory:")
    for i in inventory:
        print(i)
        
    cursor.execute('SELECT * FROM Orders')
    orders = cursor.fetchall()
    print("\nOrders:")
    for o in orders:
        print(o)

conn.close()