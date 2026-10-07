import pandas as pd
#import matplotlib.pyplot as plt


tables = pd.read_html("C:/Users/Acer/Downloads/List of largest companies in India - Wikipedia.html")

df = tables[0]

df['Revenue'] = pd.to_numeric(df['Revenue (billions US$)'], errors='coerce')

'''total_revenue = df['Revenue'].sum()

df['Market Share (%)'] = (df['Revenue'] / total_revenue) * 100 # Calculate market share

df_sorted = df.sort_values('Market Share (%)', ascending=False) # Sort top 10 companies
print(df_sorted[['Name', 'Revenue', 'Market Share (%)']].head(10)) 

industry_revenue = df.groupby('Industry')['Revenue'].sum().reset_index()
total_revenue = industry_revenue['Revenue'].sum()
industry_revenue['Market Share (%)'] = (industry_revenue['Revenue'] / total_revenue) * 100
industry_sorted = industry_revenue.sort_values('Market Share (%)', ascending=False)
print(industry_sorted)

plt.figure(figsize=(10,6))
plt.barh(industry_sorted['Industry'], industry_sorted['Market Share (%)'], color='teal')
plt.xlabel("Market Share (%)")
plt.title("Market Share by Industry Sector (Based on Revenue)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()'''

hq_revenue = df.groupby('Headquarters')['Revenue'].sum().reset_index()
total_revenue = hq_revenue['Revenue'].sum()
hq_revenue['Market Share (%)'] = (hq_revenue['Revenue'] / total_revenue) * 100
hq_sorted = hq_revenue.sort_values('Market Share (%)', ascending=False)
print(hq_sorted.head(10))