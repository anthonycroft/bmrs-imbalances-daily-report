from datetime import datetime, timedelta

import pandas as pd

# import Dash components
from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP
from pandas import DataFrame
from src.components.layout import create_layout
from src.data.cleaner import clean_data
from src.data.fetcher import fetch_data


class ImbalanceReportGenerator:
    """Generates and displays an imbalance report from the cleaned data."""

    def __init__(self, df: DataFrame):
        self.df = df

    def calculate_imbalance_cost(self) -> None:
        """Calculates the imbalance cost and unit rate for the report."""

        # Imbalance cost (nets long and short positions)
        self.df["imbalanceCost"] = self.df.apply(
            lambda row: (row["volume"] * row["price"]), axis=1
        )

        # Imbalance cost (no netting of long and short positions)
        self.df["imbalanceCostAbsolute"] = self.df.apply(
            lambda row: (abs(row["volume"]) * row["price"]), axis=1
        )

    def generate_report(self) -> None:
        """Generates a summary of the total daily imbalance cost and unit rate."""

        net_imbalance_cost = self.df["imbalanceCost"].sum()  # net position cost
        total_daily_cost = self.df[
            "imbalanceCostAbsolute"
        ].sum()  # cost of short and long positions
        total_absolute_volume = self.df["volume"].abs().sum()  # total absolute volume

        # Calculate the daily imbalance unit rate
        daily_imbalance_unit_rate = (
            (total_daily_cost / total_absolute_volume)
            if total_absolute_volume != 0
            else 0
        )

        # Print summary report
        print(f"Total Daily Imbalance Cost: £{net_imbalance_cost:,.0f}")
        print(f"Daily Imbalance Unit Rate: £{daily_imbalance_unit_rate:,.2f} per MWh")


class TimeSeriesFetcher:
    """Returns either pice or volume as a pandas series"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def fetch_series(self, column: str) -> pd.Series:
        return self.df[column]


class CreatePlots:
    """Creates a visualization of the data"""

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def create_plot(self) -> None:
        app = Dash(external_stylesheets=[BOOTSTRAP])
        app.title = "Daily Imbalance Report"
        app.layout = create_layout(app, self.data)
        app.run()


def main():
    # Initialize df_clean outside the try block
    df_clean = None

    # Set the report date to yesterday
    r_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        # ------------------------------------------------------
        # Format and clean the data
        # ------------------------------------------------------
        # Attempt to fetch and format the data
        df_shaped = fetch_data(r_date)
        print("Data fetched and formatted successfully.")

        # Clean the data
        df_clean = clean_data(df_shaped)
        print("Data cleaned successfully.")

        # Continue with further processing of `data` (e.g., cleaning or analysis)

    except ValueError as e:
        # Catch any ValueErrors thrown during fetch and format
        print(f"Error: {e}")

    except Exception as e:
        # General catch-all for any unexpected errors
        print(f"An unexpected error occurred: {e}")

    # ------------------------------------------------------

    # Generate report

    # Ensure df_clean is not None before generating report or plotting
    if df_clean is not None:
        report = ImbalanceReportGenerator(df_clean)
        report.calculate_imbalance_cost()
        report.generate_report()

        plotter = CreatePlots(df_clean)
        plotter.create_plot()
    else:
        print("No data available for reporting or plotting due to previous errors.")


# Main flow for generating the report
if __name__ == "__main__":
    main()
