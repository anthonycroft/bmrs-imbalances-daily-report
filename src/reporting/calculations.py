import pandas as pd


def calculate_absolute_volume(df: pd.DataFrame) -> None:
    # Imbalance cost (nets long and short positions)
    df["absoluteVolume"] = df.apply(lambda row: (abs(row["volume"])), axis=1)


# calculates Net and Absolute Imbalance Cost columns
def calculate_imbalance_cost(df: pd.DataFrame) -> None:
    """Calculates the imbalance cost and unit rate for the report."""

    # Imbalance cost (nets long and short positions)
    df["imbalanceCost"] = df.apply(lambda row: (row["volume"] * row["price"]), axis=1)

    # Imbalance cost (no netting of long and short positions)
    df["imbalanceCostAbsolute"] = df.apply(
        lambda row: (abs(row["volume"]) * row["price"]), axis=1
    )


def net_imbalance_cost_total(df: pd.DataFrame) -> float:
    """Calculates total daily imbalance"""

    # net position cost
    return df["imbalanceCost"].sum()


def daily_imbalance_unit_rate(df: pd.DataFrame) -> float:
    """Calculates total daily imbalance unit rate."""

    # total absolute volume
    total_absolute_volume = df["absoluteVolume"].sum()

    # Calculate the daily imbalance unit rate
    return (
        (df["imbalanceCostAbsolute"].sum() / total_absolute_volume)
        if total_absolute_volume != 0
        else 0
    )


def calculate_hour(df: pd.DataFrame) -> float:
    # Ensure startTime is in datetime format
    df["startTime"] = pd.to_datetime(df["startTime"])

    # Extract the hour from startTime and add it as a new column
    df["hour"] = df["startTime"].dt.floor("h")

    # Group by settlementDate and hour, then sum absoluteVolume
    hourly_volumes = df.groupby(["date", "hour"])["absoluteVolume"].sum().reset_index()

    # Identify the hour with the maximum absolute imbalance volume
    return hourly_volumes.loc[hourly_volumes["absoluteVolume"].idxmax()]


def create_calculated_columns(df: pd.DataFrame) -> None:
    calculate_absolute_volume(df)
    calculate_imbalance_cost(df)
