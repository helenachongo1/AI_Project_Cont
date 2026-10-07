import pandas as pd
import matplotlib.pyplot as plt

path=r"C:\Users\Acer\Downloads\Sample - Superstore-2.xlsx"
df = pd.read_excel(path, index_col=None, parse_dates=["Order Date"])

df["Year-Month"] = df["Order Date"].dt.to_period("M") 
monthly_data = df.groupby("Year-Month")[["Sales", "Profit"]].sum().reset_index()

monthly_data["Year-Month"] = monthly_data["Year-Month"].astype(str)
monthly_data["Year-Month"] = pd.to_datetime(monthly_data["Year-Month"])

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(monthly_data["Year-Month"], monthly_data["Profit"], color="lightgreen", alpha=0.7, label="Profit", width=20)
ax1.set_ylabel("Profit (USD)", color="green")
ax1.tick_params(axis="y", labelcolor="green")

ax2 = ax1.twinx()
ax2.plot(monthly_data["Year-Month"], monthly_data["Sales"], color="blue", marker="o", linestyle="-", label="Sales")
ax2.set_ylabel("Sales (USD)", color="blue")
ax2.tick_params(axis="y", labelcolor="blue")

plt.title("Sales (Line Chart) & Profit (Bar Chart) Over Time")
ax1.set_xlabel("Order Date (Year-Month)")
plt.xticks(rotation=45)
ax1.grid(True, linestyle="--", alpha=0.5)

ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

plt.show()