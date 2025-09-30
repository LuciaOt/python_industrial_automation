# Import libraries
import pandas as pd
import plotly.graph_objects as go

PATH = "datasets/robot_imu_comparison/R1.csv"
# Load the dataset
dataset = pd.read_csv(PATH)
dataset.rename(
    columns={
        r"Time": "time",
        r"Position\X Position In Current Wobj": "pos_x",
        r"Position\Y Position In Current Wobj": "pos_y",
        r"Position\Z Position In Current Wobj": "pos_z",
    },
    inplace=True,
)
fig = go.Figure()
fig.add_trace(
    go.Scatter3d(
        x=dataset["pos_x"],
        y=dataset["pos_y"],
        z=dataset["pos_z"],
        mode="lines",
        line=dict(color="blue", width=2),
        name="Path",
    )
)
fig.add_trace(
    go.Scatter3d(
        x=dataset["pos_x"],
        y=dataset["pos_y"],
        z=dataset["pos_z"],
        mode="markers",
        marker=dict(
            color=dataset["time"],
            colorscale="viridis",
            size=3,
            colorbar=dict(title="Time"),
        ),
        name="Points",
    )
)
fig.show()
