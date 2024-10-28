import pandas as pd
import requests

from datetime import datetime
from . import ids


"""Fetches and formats the data i.e. concerned with columns.
See also cleaner.py for cleansing (row) processing"""


def get_raw_data(r_date: datetime) -> dict:
    """Fetches the data for the specified date and returns it as a DataFrame."""

    endpoint = f"{ids.BASE_URL}{r_date}?format=json"
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
        col for col in ids.EXPECTED_TYPES.keys() if col not in raw_data["data"][0]
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

    return df


def column_selector(df: pd.DataFrame) -> pd.DataFrame:
    # Select only columns defined in REQUIRED_COLUMNS_RENAMER and rename them
    return df[list(ids.REQUIRED_COLUMNS_RENAMER.keys())].rename(columns=ids.REQUIRED_COLUMNS_RENAMER)


def enforce_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensures correct datatypes for expected columns."""

    for column, expected_type in ids.EXPECTED_TYPES.items():
        try:
            df[column] = df[column].astype(expected_type)
        except ValueError as e:
            raise ValueError(
                f"Column '{column}' could not be cast to {expected_type}. Error: {e}"
            )
    return df


def fetch_data(r_date: datetime) -> pd.DataFrame:
    """Fetches and formats the imbalance data as a DataFrame."""

    # fetch the data via API
    raw_data = get_raw_data(r_date)

    # Convert the raw data to a DataFrame
    df = to_dataframe(raw_data)
    # Ensure correct data types
    df = enforce_data_types(df)
    # Select only required columns and rename them
    df = column_selector(df)
    print(df)



    return df
