import plotly.graph_objects as go
import pandas as pd

# Create the data
data = [
    {"component": "User Mobile App", "type": "input", "x": 1, "y": 4},
    {"component": "BLE Beacons", "type": "sensor", "x": 2, "y": 3},
    {"component": "Wi-Fi Network", "type": "sensor", "x": 2, "y": 5},
    {"component": "Backend Engine", "type": "processing", "x": 4, "y": 4},
    {"component": "Gate Detection", "type": "decision", "x": 5, "y": 4},
    {"component": "Valet Dashboard", "type": "output", "x": 6, "y": 3},
    {"component": "Car Dispatch", "type": "action", "x": 6, "y": 5},
    {"component": "Gate A", "type": "location", "x": 7, "y": 2},
    {"component": "Gate B", "type": "location", "x": 7, "y": 3},
    {"component": "Gate C", "type": "location", "x": 7, "y": 4},
    {"component": "Gate D", "type": "location", "x": 7, "y": 5}
]

df = pd.DataFrame(data)

# Define colors for different component types
colors = {
    'input': '#1FB8CD',
    'sensor': '#DB4545', 
    'processing': '#2E8B57',
    'decision': '#5D878F',
    'output': '#D2BA4C',
    'action': '#B4413C',
    'location': '#964325'
}

# Define symbols for different component types
symbols = {
    'input': 'square',
    'sensor': 'square',
    'processing': 'square',
    'decision': 'diamond',
    'output': 'square',
    'action': 'square',
    'location': 'circle'
}

# Create the figure
fig = go.Figure()

# Add traces for each component type
for comp_type in df['type'].unique():
    type_data = df[df['type'] == comp_type]
    
    fig.add_trace(go.Scatter(
        x=type_data['x'],
        y=type_data['y'],
        mode='markers+text',
        marker=dict(
            size=25,
            color=colors[comp_type],
            symbol=symbols[comp_type],
            line=dict(width=2, color='white')
        ),
        text=type_data['component'],
        textposition='bottom center',
        textfont=dict(size=9),
        name=comp_type.title(),
        hovertemplate='%{text}<br>Type: ' + comp_type + '<extra></extra>'
    ))

# Add flow arrows between components
flow_connections = [
    # User -> Sensors
    {'start': (1, 4), 'end': (2, 3), 'label': 'Location'},
    {'start': (1, 4), 'end': (2, 5), 'label': 'Connect'},
    # Sensors -> Backend
    {'start': (2, 3), 'end': (4, 4), 'label': 'Signal'},
    {'start': (2, 5), 'end': (4, 4), 'label': 'Data'},
    # Backend -> Decision
    {'start': (4, 4), 'end': (5, 4), 'label': 'Process'},
    # Decision -> Outputs
    {'start': (5, 4), 'end': (6, 3), 'label': 'Update'},
    {'start': (5, 4), 'end': (6, 5), 'label': 'Dispatch'},
    # Outputs -> Gates
    {'start': (6, 3), 'end': (7, 2), 'label': 'Valet A'},
    {'start': (6, 3), 'end': (7, 3), 'label': 'Valet B'},
    {'start': (6, 5), 'end': (7, 4), 'label': 'Car C'},
    {'start': (6, 5), 'end': (7, 5), 'label': 'Car D'}
]

# Add arrows for data flow
for conn in flow_connections:
    start_x, start_y = conn['start']
    end_x, end_y = conn['end']
    
    # Add arrow line
    fig.add_trace(go.Scatter(
        x=[start_x, end_x],
        y=[start_y, end_y],
        mode='lines',
        line=dict(color='gray', width=2),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add arrowhead
    fig.add_annotation(
        x=end_x,
        y=end_y,
        ax=start_x,
        ay=start_y,
        xref='x',
        yref='y',
        axref='x',
        ayref='y',
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor='gray',
        showarrow=True,
        text=''
    )

# Update layout
fig.update_layout(
    title="Valet Parking System Architecture",
    xaxis_title="System Flow",
    yaxis_title="Component Layer",
    showlegend=True,
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5),
    xaxis=dict(range=[0, 8], showgrid=True, gridwidth=1, gridcolor='lightgray'),
    yaxis=dict(range=[1, 6], showgrid=True, gridwidth=1, gridcolor='lightgray')
)

# Save the chart
fig.write_image("valet_parking_architecture.png")