import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from . import ids

"""
Renders a Line chart
"""

def render_line_chart(app: Dash, data: pd.DataFrame, y_column: str, title: str, y_label: str) -> html.Div:
    """Renders a generic line chart for a given column in the data."""

    if data.empty:
        return html.Div(f"No data available for {y_column}.", id=f"{ids.LINE_CHART}-{y_column}")

    # Plot the specified column against 'startTime'
    fig = px.line(
        data,
        x="startTime",
        y=y_column,
        title=title,
        labels={y_column: y_label, "startTime": "startTime"},
    )

    fig.update_layout(margin=dict(t=50), title_x=0.5)
    
    return html.Div(dcc.Graph(figure=fig), id=f"{ids.LINE_CHART}-{y_column}")
