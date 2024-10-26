import pandas as pd
from dash import Dash, html

from . import line_chart

def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            line_chart.render_line_chart(app, data, y_column="price", title="System Buy/Sell Prices Over Time", y_label="Price (£)"),
            html.Br(),
            line_chart.render_line_chart(app, data, y_column="volume", title="System Volume Over Time", y_label="Volume (MWh)"),
        ],
        style={"text-align": "center", "padding": "2%"},
    )