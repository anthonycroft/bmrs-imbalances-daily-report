from datetime import datetime, timedelta

import pandas as pd

# import Dash components
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from components.layout import create_layout
from data.cleaner import clean_data
from data.fetcher import fetch_data
from reporting.reporter import create_imbalance_report

"""
Main Program
"""


class TimeSeriesFetcher:
    """Returns a series present in the dataframe - for future use"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def fetch_series(self, column: str) -> pd.Series:
        return self.df[column]


def main():
    """Runs the application"""

    # Initialize df_clean outside the try block
    df_clean = None

    # Set the report date to yesterday
    r_date = (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d")

    # ------------------------------------------------------
    # Format and clean the data
    # ------------------------------------------------------
    try:
        # Attempt to fetch and format the data
        df_shaped = fetch_data(r_date)
        print("Data fetched and formatted successfully.")

        # Clean the data
        df_clean = clean_data(df_shaped)
        print("Data cleaned successfully.")

    except ValueError as e:
        # Catch any ValueErrors thrown during fetch and format
        print(f"Error: {e}")

    except Exception as e:
        # General catch-all for any unexpected errors
        print(f"An unexpected error occurred: {e}")
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Generate report
    # ------------------------------------------------------
    # Ensure df_clean is not None before generating report or plotting
    if df_clean is not None:
        # Calculate the imbalance cost and unit rate
        create_imbalance_report(df_clean)

        # create visualisations
        app = Dash(external_stylesheets=[BOOTSTRAP])
        app.title = "Daily Imbalance Cost Report"
        app.layout = create_layout(app, df_clean)
        app.run()
    else:
        print("No data available for reporting or plotting due to previous errors.")


# Main flow for generating the report
if __name__ == "__main__":
    main()
