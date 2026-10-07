import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import folium
#from geopy.geocoders import Nominatim
#import plotly.express as px

#Question 1
'''df = pd.read_excel("C:/Users/Acer/Downloads/Sample - Superstore-4.xlsx")
df_subset = df[['Region','Sub-Category','Segment','Profit']]

df_pivot = df_subset.groupby(['Region','Sub-Category','Segment'])['Profit'].sum().reset_index()

df_pivot_table = df_pivot.pivot_table(values='Profit',
                                      index=['Sub-Category'],
                                      columns=['Region','Segment'],
                                      aggfunc='sum')

plt.figure(figsize=(12, 8))
sns.heatmap(df_pivot_table, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5, center=0)

plt.title("Profit Variation Across Regions, Sub-Categories, and Segments")
plt.xlabel("Region vs Customer Segment")
plt.ylabel("Product Sub-Category")
plt.xticks(rotation=45, ha="right")  
plt.yticks(rotation=0)
plt.show()'''

#Question 2
'''df = pd.read_excel("C:/Users/Acer/Downloads/Sample - Superstore-4.xlsx")
state_reg = df[['State','Region']].drop_duplicates()
geolocator = Nominatim(user_agent="geoapiExercises")

def get_coord(state):
    try:
        location = geolocator.geocode(state + ", USA")
        return pd.Series([location.latitude, location.longitude])
    except:
        return pd.Series([None,None])
    
state_reg[['Latitude', 'Longitude']] = state_reg['State'].apply(get_coord)

superstore_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

for _, row in state_reg.iterrows():
    if pd.notnull(row['Latitude']) and pd.notnull(row['Longitude']):
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"State: {row['State']}<br>Region: {row['Region']}",
            tooltip=row['State']
        ).add_to(superstore_map)
        
superstore_map

state_sales = df.groupby("State")["Sales"].sum().reset_index()
fig = px.choropleth(state_sales,
                    locations="State",
                    locationmode="USA-states",
                    color="Sales",
                    scope="usa",
                    title="Total Sales by State (Superstore Dataset)",
                    color_continuous_scale="blues")

fig.show()'''

#Question 3
df = pd.read_excel("C:/Users/Acer/Downloads/Sample - Superstore-4.xlsx")
df_subset = df[['State','Category','Sales']]

df_pivot = df.pivot_table(values='Sales', index='State', columns='Category', aggfunc='sum')

plt.figure(figsize=(8, 6))
sns.heatmap(df_pivot, cmap='coolwarm', annot=True, fmt=".0f", linewidths=0.5)
plt.title("Sales Density Heatmap")
plt.xlabel("Category")
plt.ylabel("Location")
plt.show()

