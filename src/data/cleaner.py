import pandas as pd
from . import ids

"""Formats imported data according to expected columns and data types."""

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
