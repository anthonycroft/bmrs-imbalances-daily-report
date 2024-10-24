from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests
from pandas import DataFrame
from scipy import stats

# calculate yesterday's date
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# endpoint for Indicative Imbalance Settlement
BMRS_API_ENDPOINT = f"https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{yesterday}?format=json"


# Function to get system imbalance cost and price
def get_system_imbalance_data() -> DataFrame:
    # Calculate previous day (BMRS typically updates for previous day)

    # Make the GET request to retrieve the imbalance data
    response = requests.get(f"{BMRS_API_ENDPOINT}")

    # Check if request was successful
    if response.status_code == 200:
        # Parse the response
        data = response.json()

        # Load data into a pandas DataFrame
        df = pd.DataFrame(data["data"])[
            [
                "settlementDate",
                "settlementPeriod",
                "startTime",
                "systemSellPrice",
                "systemBuyPrice",
                "netImbalanceVolume",
            ]
        ]

        # Return the DataFrame for further use
        return df

    else:
        print(f"Error: Unable to fetch data, Status code {response.status_code}")

    # Return None if request was unsuccessful
    return None


def clean_data(df: DataFrame) -> DataFrame:
    # Check for 48 rows:

    # Strip white space from coiumn names
    df.columns = df.columns.str.strip()

    df.isnull().sum()  # Check for missing values
    df.dropna()  # Drop rows with missing values

    # Convert columns to appropriate data types
    df["settlementDate"] = pd.to_datetime(df["settlementDate"])
    df["startTime"] = pd.to_datetime(df["startTime"])

    # Filter out rows with negative values
    df = df[df["systemSellPrice"] >= 0]
    df = df[df["systemBuyPrice"] >= 0]

    # Basic method to check for outliers using z-score
    df = df[
        (
            np.abs(
                stats.zscore(
                    df[["systemSellPrice", "systemBuyPrice", "netImbalanceVolume"]]
                )
            )
            < 3
        ).all(axis=1)
    ]

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Sort the DataFrame by date and period
    df.sort_values(by=["settlementDate", "settlementPeriod"], inplace=True)

    # Round the 'systemBuyPrice' and 'systemSellPrice' columns to 2 decimal places
    df["systemBuyPrice"] = df["systemBuyPrice"].round(2)
    df["systemSellPrice"] = df["systemSellPrice"].round(2)
    df["netImbalanceVolume"] = df["netImbalanceVolume"].round(2)

    # Rename columns for consistency
    df.rename(
        columns={
            "settlementDate": "date",
            "settlementPeriod": "period",
            "systemSellPrice": "sellPrice",
            "systemBuyPrice": "buyPrice",
            "netImbalanceVolume": "volume",
        },
        inplace=True,
    )

    # Check the number of rows in the DataFrame
    row_count = df.shape[0]
    print(f"Number of rows: {row_count}")

    return df


if __name__ == "__main__":
    df = get_system_imbalance_data()
    df_clean = clean_data(df)

    # Print the DataFrame for review
    print(df_clean)
