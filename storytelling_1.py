import pandas as pd
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

df = pd.read_excel("C:/Users/Acer/OneDrive/Desktop/ICT_2025/DVD/Sample - Superstore-5.xlsx")

fig = px.scatter(df,
                 x="Sales", y="Profit",
                 color="Category",
                 size="Quantity",
                 hover_data=["Sub-Category", "Region", "Order Date"],
                 title="Profit vs. Sales by Category")
fig.show()

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Year"] = df["Order Date"].dt.year

fig = px.scatter(df,
                 x="Sales", y="Profit",
                 color="Category", size="Quantity",
                 animation_frame="Year",
                 hover_data=["Sub-Category"],
                 title="Profit vs. Sales Over Time")
fig.show()