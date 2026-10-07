import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm

df = pd.read_excel("C:/Users/Acer/Downloads/Air Quality Data (1).xlsx")
df.dropna(inplace=True)

#print(df.info())
#print(df.describe())

#mean_x1 = df['so2'].mean()
#print("The mean of so2:", mean_x1)

#sns.histplot(df['so2'], kde=True)
#plt.title("Histogram of SO2")
#plt.show()

pollutant = df[['so2','no2','rspm']]
correlation_matrix = pollutant.corr()
print(correlation_matrix)

plt.figure(figsize=(8,6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation between pollutants')
plt.show()




