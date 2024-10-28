import pandas as pd

"""
Data cleansing routines. Concerned with rows rather than columns.
See fetcher.py for column level processing
"""

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
