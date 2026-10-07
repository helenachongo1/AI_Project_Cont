import pandas as pd
import matplotlib.pyplot as plt

path=r"C:\Users\Acer\Downloads\Sample - Superstore-2.xlsx"
df = pd.read_excel(path, index_col=None, parse_dates=["Order Date"])

df["Year-Month"] = df["Order Date"].dt.to_period("M") 
monthly_data = df.groupby("Year-Month")[["Sales", "Profit", "Quantity"]].sum().reset_index()

monthly_data["Year-Month"] = monthly_data["Year-Month"].astype(str)
monthly_data["Year-Month"] = pd.to_datetime(monthly_data["Year-Month"])

plt.figure(figsize=(12, 6))

plt.stackplot(monthly_data["Year-Month"], 
              monthly_data["Sales"], 
              monthly_data["Profit"], 
              monthly_data["Quantity"], 
              labels=["Sales", "Profit", "Quantity"], 
              colors=["skyblue", "lightgreen", "salmon"], 
              alpha=0.7)

plt.xlabel("Order Date (Year-Month)")
plt.ylabel("Values")
plt.title("Stacked Line Chart of Sales, Profit & Quantity Over Time")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)

plt.show()