# test_calculations.py
"""Performs tests against a sample test file (tests/test_data.csv) which contains
pre-calculated values for intermediary columns and final output values required
by the Daily Imbalnace Cost Rerport

The tests check that calculated columns contain the correct value for each time period
and that the final output values match the expected values.
"""

import pandas as pd
import pytest
from src.reporting.calculations import (
    create_calculated_columns,
    daily_imbalance_unit_rate,
    net_imbalance_cost_total,
)

# Define the data types for each column
data_types = {
    "settlementDate": str,
    "settlementPeriod": str,
    "startTime": str,
    "price": float,
    "volume": float,
    "expected_imbalanceVolumeAbsolute": float,
    "expected_imbalanceCost": float,
    "expected_imbalanceCostAbsolute": float,
    "expected_daily_imbalance_unit_rate": float,
    "expected_net_imbalance_cost": float,
}


def pre_processing():
    # Load the sample data
    df = load_test_data()

    # Run the calculation function to add imbalance cost columns
    create_calculated_columns(df)

    return df


@pytest.fixture
def df():
    """Fixture to load the sample data and create calculated columns."""
    df = load_test_data()
    create_calculated_columns(df)
    return df


# Load the test data from CSV
def load_test_data(file_path="tests/test_data.csv"):
    return pd.read_csv(file_path, dtype=data_types)


@pytest.mark.parametrize(
    "calculated_col, expected_col",
    [
        ("absoluteVolume", "expected_imbalanceVolumeAbsolute"),
        ("imbalanceCost", "expected_imbalanceCost"),
        ("imbalanceCostAbsolute", "expected_imbalanceCostAbsolute"),
    ],
)
def test_calculated_columns(df, calculated_col, expected_col):
    pd.testing.assert_series_equal(
        df[calculated_col].round(2), df[expected_col].round(2), check_names=False
    )


def test_net_imbalance_cost_total(df):
    # Load the sample data and create tool calculated columns
    df = pre_processing()

    # Run the calculation for net imbalance cost total
    calculated_nic_total = net_imbalance_cost_total(df)

    # Assert that the calculated value matches the expected value
    assert (
        round(calculated_nic_total, 0)
        == round(df["expected_net_imbalance_cost"].iloc[0], 0)
    ), f"Expected {round(df['expected_net_imbalance_cost'].iloc[0],0)}, got {round(calculated_nic_total,0)}"


def test_daily_imbalance_unit_rate():
    # Load the sample data and create tool calculated columns
    df = pre_processing()

    # Run the calculation for daily imbalance unit rate
    calculated_dir = daily_imbalance_unit_rate(df)

    # Assert that the calculated value matches the expected value
    assert (
        round(calculated_dir, 2)
        == round(df["expected_daily_imbalance_unit_rate"].iloc[0], 2)
    ), f"Expected {round(df['expected_daily_imbalance_unit_rate'].iloc[0],2)}, got {round(calculated_dir,2)}"


if __name__ == "__main__":
    pytest.main()
