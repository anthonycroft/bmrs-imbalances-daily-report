
import pandas as pd
import requests

from datetime import datetime
from . import ids


def get_raw_data(r_date: datetime) -> dict:
    """Fetches the data for the specified date and returns it as a DataFrame."""

    # r_date = date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

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

    # Select only columns defined in COLUMN_RENAMER and rename them
    df = df[list(ids.COLUMN_RENAMER.keys())].rename(columns=ids.COLUMN_RENAMER)

    return df


def fetch_data(r_date: datetime) -> pd.DataFrame:
    """Fetches and formats the imbalance data as a DataFrame."""

    raw_data = get_raw_data(r_date)

    df = to_dataframe(raw_data)
    # After final cleaning and before passing the DataFrame for analysis
    # df.set_index("startTime", inplace=True)

    return df
