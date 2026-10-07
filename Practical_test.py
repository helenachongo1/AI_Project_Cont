import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("C:/Users/Acer/Downloads/Air Quality Data (1).xlsx")

avg_no2_emissions = df.groupby('type')['no2'].mean()

'''plt.figure(figsize=(8, 5))
avg_no2_emissions.plot(kind='bar', color='blue', edgecolor='black')
plt.title('Average NO₂ Emissions Across Sector')
plt.xlabel('Sector')
plt.ylabel('Average NO₂ Emissions')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()'''

'''sns.histplot(df['no2'], kde=True)
plt.title('no2 Distribution')
plt.show()'''

#print(df.describe())
#print(df.info())

pollutants = df[['so2', 'no2', 'rspm', 'spm', 'pm2_5']]
correlation_matrix = pollutants.corr()
print(correlation_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Between Pollutants')
plt.show()