# Install dash if needed:
# pip install dash

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.graph_objects as go
import random
from collections import deque

# Initialize Dash app
app = dash.Dash(__name__)

# Use deque for efficient data updates (fixed-length queue)
max_length = 20
x_data = deque(maxlen=max_length)
y_data = deque(maxlen=max_length)

# Initialize empty figure with one scatter trace
fig = go.Figure()
fig.add_scatter(
    x=list(x_data), y=list(y_data), mode="lines+markers", name="Random Data"
)

# App layout: title, graph, and interval component for updates
app.layout = html.Div(
    [
        html.H1("Live Updating Plotly Graph"),
        dcc.Graph(id="live-graph", figure=fig),
        dcc.Interval(
            id="interval-component", interval=1000, n_intervals=0  # 1000ms = 1 second
        ),
    ]
)


# Callback to update graph every interval
@app.callback(
    Output("live-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_graph(n):
    # Append new data point
    x_data.append(n)
    y_data.append(random.randint(0, 10))  # simulate new data
    # Create new figure with updated data
    fig = go.Figure()
    fig.add_scatter(
        x=list(x_data), y=list(y_data), mode="lines+markers", name="Random Data"
    )
    fig.update_layout(xaxis_title="Time (s)", yaxis_title="Value")
    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
