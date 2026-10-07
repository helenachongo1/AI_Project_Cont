import pandas as pd
import matplotlib.pyplot as plt

path=r"C:\Users\Acer\Downloads\Sample - Superstore-2.xlsx"
df = pd.read_excel(path, index_col=None, parse_dates=["Order Date"])

df["Year-Month"] = df["Order Date"].dt.to_period("M") 
monthly_data = df.groupby("Year-Month")[["Sales", "Profit"]].sum().reset_index()

monthly_data["Year-Month"] = monthly_data["Year-Month"].astype(str)
monthly_data["Year-Month"] = pd.to_datetime(monthly_data["Year-Month"])

plt.figure(figsize=(12, 6))
plt.fill_between(monthly_data["Year-Month"], monthly_data["Sales"], color="skyblue", alpha=0.5, label="Sales")
plt.fill_between(monthly_data["Year-Month"], monthly_data["Sales"] + monthly_data["Profit"], monthly_data["Sales"], 
                 color="lightgreen", alpha=0.7, label="Profit")

plt.xlabel("Order Date (Year-Month)")
plt.ylabel("Amount (USD)")
plt.title("Stacked Line Chart of Sales & Profit Over Time")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.show()
