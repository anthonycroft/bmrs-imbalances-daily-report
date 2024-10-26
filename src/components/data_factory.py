from datetime import datetime, timedelta

import pandas as pd
import requests

"""Formats imported data according to expected columns and data types."""

EXPECTED_TYPES = {
    "settlementDate": "datetime64[ns]",
    "settlementPeriod": "int64",
    "startTime": "datetime64[ns, UTC]",
    "systemSellPrice": "float64",
    "systemBuyPrice": "float64",
    "netImbalanceVolume": "float64",
}

COLUMN_RENAMER = {
    "startTime": "startTime",
    "systemSellPrice": "price",
    "netImbalanceVolume": "volume",
}

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/"


def get_raw_data(date: datetime) -> dict:
    """Fetches the data for the specified date and returns it as a DataFrame."""

    r_date = date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    endpoint = f"{BASE_URL}{r_date}?format=json"
    response = requests.get(endpoint)

    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error fetching data, status code {response.status_code}")


def validate_columns(raw_data: dict) -> None:
    """Checks that all expected columns are in the data response."""

    if "data" not in raw_data:
        raise ValueError("Unexpected data format: 'data' key not found in response.")

    missing_columns = [
        col for col in EXPECTED_TYPES.keys() if col not in raw_data["data"][0]
    ]
    if missing_columns:
        raise ValueError(
            f"Missing expected columns in data response: {missing_columns}"
        )


def to_dataframe(raw_data: dict) -> pd.DataFrame:
    """Converts raw data dictionary to a DataFrame with the expected columns."""

    validate_columns(raw_data)  # Ensure expected columns are present

    # Convert raw data to DataFrame
    df = pd.DataFrame(raw_data["data"])

    # Select only columns defined in COLUMN_RENAMER and rename them
    df = df[list(COLUMN_RENAMER.keys())].rename(columns=COLUMN_RENAMER)

    return df


def enforce_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures correct datatypes for expected columns."""

    for column, expected_type in EXPECTED_TYPES.items():
        try:
            df[column] = df[column].astype(expected_type)
        except ValueError as e:
            raise ValueError(
                f"Column '{column}' could not be cast to {expected_type}. Error: {e}"
            )
    return df


def fetch_data(r_date: datetime) -> pd.DataFrame:
    """Fetches and formats the imbalance data as a DataFrame."""

    raw_data = get_raw_data(r_date)

    df = to_dataframe(raw_data)
    # After final cleaning and before passing the DataFrame for analysis
    df.set_index("startTime", inplace=True)

    return df


"""Data cleansing routines."""


def remove_na(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows with any NA or NaN values."""
    return df.dropna()


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows."""
    return df.drop_duplicates()


def sort_by_time(df: pd.DataFrame) -> pd.DataFrame:
    """Sorts DataFrame by the 'startTime' column."""
    return df.sort_values(by="startTime")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Performs data cleaning: removes NAs, removes duplicates, and sorts by time."""
    df = remove_na(df)
    df = remove_duplicates(df)
    df = sort_by_time(df)
    return df
