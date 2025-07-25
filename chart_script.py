import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Create the data
data = [
    {"Technology": "BLE Beacons", "Accuracy_meters": 3, "Cost_scale": 2, "Battery_life_years": 2, "Maintenance": "Medium"},
    {"Technology": "Wi-Fi Triangulation", "Accuracy_meters": 10, "Cost_scale": 1, "Battery_life_years": 0, "Maintenance": "Low"},
    {"Technology": "GPS Indoor", "Accuracy_meters": 8, "Cost_scale": 1, "Battery_life_years": 0, "Maintenance": "Low"},
    {"Technology": "IMU Sensor Fusion", "Accuracy_meters": 2.5, "Cost_scale": 1, "Battery_life_years": 0, "Maintenance": "Very Low"}
]

df = pd.DataFrame(data)

# Map maintenance levels to marker sizes
maintenance_size_map = {
    "Very Low": 15,
    "Low": 25, 
    "Medium": 35,
    "High": 45
}

df['marker_size'] = df['Maintenance'].map(maintenance_size_map)

# Abbreviate technology names to fit 15 char limit
df['Tech_abbrev'] = df['Technology'].apply(lambda x: 
    x.replace('BLE Beacons', 'BLE Beacons')
    .replace('Wi-Fi Triangulation', 'Wi-Fi Triang')
    .replace('GPS Indoor', 'GPS Indoor')
    .replace('IMU Sensor Fusion', 'IMU Sensor')
)

# Define colors from the brand palette
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F']

# Create scatter plot
fig = go.Figure()

for i, (idx, row) in enumerate(df.iterrows()):
    fig.add_trace(go.Scatter(
        x=[row['Cost_scale']],
        y=[row['Accuracy_meters']],
        mode='markers',
        marker=dict(
            size=row['marker_size'],
            color=colors[i % len(colors)],
            line=dict(width=2, color='white')
        ),
        name=row['Tech_abbrev'],
        hovertemplate='<b>%{fullData.name}</b><br>' +
                     'Cost: %{x}<br>' +
                     'Accuracy: %{y}m<br>' +
                     'Maintenance: ' + row['Maintenance'] + '<extra></extra>',
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title="Indoor Position Tech Comparison",
    xaxis_title="Cost Scale",
    yaxis_title="Accuracy (m)",
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    )
)

# Update axes
fig.update_xaxes(
    range=[0.5, 5.5],
    tickvals=[1, 2, 3, 4, 5]
)

fig.update_yaxes(
    range=[0, 12]
)

# Save the chart
fig.write_image("indoor_positioning_comparison.png")