import pandas as pd
from dash import Dash, html

from . import line_chart
from . import ids

"""
Handles the layout of the Daily Imbalance Report using components from the
Dash library
"""

def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    """Creates the layout for the Daily Imbalance Report"""
    # Create the layout
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            line_chart.render_line_chart(app, data, y_column=ids.DataSchema.PRICE, \
                title="System Buy/Sell Prices Over Time", y_label="Price (£)"),
            html.Br(),
            line_chart.render_line_chart(app, data, y_column=ids.DataSchema.VOLUME, \
                title="System Volume Over Time", y_label="Volume (MWh)"),
        ],
        style={"text-align": "center", "padding": "2%"},
    )