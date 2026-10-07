# Necessary libraries
import pandas as pd
import plotly.graph_objects as go

# Load Superstore data
df = pd.read_excel("C:/Users/Acer/OneDrive/Desktop/ICT_2025/DVD/Sample - Superstore-5.xlsx")

# Metrics to visualize
metrics = ["Sales", "Profit", "Discount", "Quantity"]

# Abbreviations for Plotly mapping
us_state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
    'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
    'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
    'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV',
    'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT',
    'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Prepare grouped data
grouped_data = {}
for metric in metrics:
    temp = df.groupby("State")[metric].sum().reset_index()
    temp["State Code"] = temp["State"].map(us_state_abbrev)
    grouped_data[metric] = temp

fig = go.Figure()

# Add traces for each metric
for i, metric in enumerate(metrics):
    fig.add_trace(go.Choropleth(
        locations=grouped_data[metric]["State Code"],
        z=grouped_data[metric][metric],
        locationmode="USA-states",
        colorscale="Plasma",
        colorbar_title=metric,
        visible=(i == 0),  # only first metric visible by default
        name=metric
    ))

# Dropdown menu
buttons = []
for i, metric in enumerate(metrics):
    visibility = [False] * len(metrics)
    visibility[i] = True
    buttons.append(dict(label=metric,
                        method="update",
                        args=[{"visible": visibility},
                              {"title": f"{metric} by U.S. State"}]))

# Updating layout with dropdown
fig.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=0.2,
        xanchor="left",
        y=1.15,
        yanchor="top"
    )],
    geo_scope='usa',
    title="Sales by U.S. State"
)

# Show it
fig.show()
