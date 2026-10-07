import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/Acer/Downloads/student_performance_dataset-1.csv")

import statsmodels.api as sm

X = df[['Study_Hours', 'Sleep_Hours', 'Attendance_Rate', 'Extracurricular_Hours', 'Screen_Time_Hours']]
X = sm.add_constant(X)  
y = df['Performance_Score']

sns.histplot(df['Study_Hours'], kde=True)
plt.title("Study Hours")
plt.show()



'''print(df.describe()) # To get the summary of the dataset

sns.pairplot(df)
plt.show()


correlation = df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()'''