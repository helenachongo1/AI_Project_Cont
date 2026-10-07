import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


sns.set(style="whitegrid")
plt.style.use('ggplot')

df = pd.read_excel("C:/Users/Acer/OneDrive/Desktop/ICT_2025/DVD/Sample - Superstore-2.xlsx")

print(df.isnull().sum()) #Checking whether there are missing values or not
df = df.drop_duplicates() #Dropping duplicates if any

#Find unique values in categorical columns
cat_cols = df.select_dtypes(include='object').columns
for col in cat_cols:
    print(f"{col}: {df[col].nunique()} unique values")

#For distribution of sales    
plt.figure(figsize=(10, 5))
sns.histplot(df['Sales'], bins=50, kde=True)
plt.title('Distribution of Sales')

#For distribution of profit
plt.figure(figsize=(10, 5))
sns.histplot(df['Profit'], bins=50, kde=True, color='blue')
plt.title('Distribution of Profits')

#Profit vs Sales
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Sales', y='Profit', hue='Category')
plt.title('Sales vs Profit by Category')

#Boxplot of Profit vs Segment
plt.figure(figsize=(8, 6))
sns.boxplot(data=df, x='Segment', y='Profit')
plt.title('Profit by Segment')

#Sales vs State
state_Sal = df.groupby('State')['Sales'].sum().sort_values(ascending=False)
plt.figure(figsize=(12, 8))
state_Sal.plot(kind='bar')
plt.title('Sum of Sales by State')
plt.ylabel('Sales')

#Sum of Sales and Profit by Category
category_prof = df.groupby('Category')[['Sales', 'Profit']].sum()
#Sub-Category analysis
plt.figure(figsize=(14, 6))
sub_cat = df.groupby('Sub-Category')['Profit'].sum().sort_values()
sub_cat.plot(kind='barh', color='red')
plt.title('Profit by Sub-Category')

#Correlation analysis
plt.figure(figsize=(8, 6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')