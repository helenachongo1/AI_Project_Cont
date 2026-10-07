import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

path = r"C:\Users\Acer\Downloads\Sample - Superstore-3.xlsx"
df = pd.read_excel(path)

plt.figure(figsize=(10, 6))
'''sns.scatterplot(x=df["Sales"], y=df["Profit"], alpha=0.6, edgecolor=None)

plt.xlabel("Sales ($)")
plt.ylabel("Profit ($)")
plt.title("Sales vs. Profit in Superstore Dataset")
plt.grid(True)

plt.show()'''

#2
'''sns.scatterplot(x=df["Sales"], y=df["Quantity"], alpha=0.6, edgecolor=None)

plt.xlabel("Sales")
plt.ylabel("Quantity")
plt.title("Sales vs. Quantity")
plt.grid(True)

plt.show()'''

#3
sns.scatterplot(x=df["Quantity"], y=df["Discount"], alpha=0.6, edgecolor=None)


plt.xlabel("Quantity")
plt.ylabel("Discount")
plt.title("Quantity vs. Discount")
plt.grid(True)

plt.show()