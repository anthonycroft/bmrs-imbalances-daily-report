# test_calculations.py

import pandas as pd
from  ..src.reporting.calculations import create_calculated_columns, net_imbalance_cost_total, daily_imbalance_unit_rate
import pytest

# Load the test data from CSV
def load_test_data(file_path="tests/data/test_calculations.csv"):
    return pd.read_csv(file_path)

def test_calculate_imbalance_cost():
    # Load the sample data
    df = load_test_data()

    # Run the calculation function to add imbalance cost columns
    # calculate_imbalance_cost(df)
    create_calculated_columns(df)

    # Check if calculated columns match the expected pre-calculated values in the CSV
    pd.testing.assert_series_equal(df["absoluteVolume"], df["expected_imbalanceVolumeAbsolute"], check_names=False)
    pd.testing.assert_series_equal(df["imbalanceCost"], df["expected_imbalanceCost"], check_names=False)
    pd.testing.assert_series_equal(df["imbalanceCostAbsolute"], df["expected_imbalanceCostAbsolute"], check_names=False)

def test_net_imbalance_cost_total():
    # Load the sample data
    df = load_test_data()

    # Run the calculation for net imbalance cost total
    calculated_nic_total = net_imbalance_cost_total(df)

    # Assert that the calculated value matches the expected value
    assert calculated_nic_total == df["expected_net_imbalance_cost"].iloc[0], \
        f"Expected {df['expected_net_imbalance_cost'].iloc[0]}, got {calculated_nic_total}"

def test_daily_imbalance_unit_rate():
    # Load the sample data
    df = load_test_data()

    # Run the calculation for daily imbalance unit rate
    calculated_dir = daily_imbalance_unit_rate(df)

    # Assert that the calculated value matches the expected value
    assert calculated_dir == df["expected_daily_imbalance_unit_rate"].iloc[0], \
        f"Expected {df['expected_daily_imbalance_unit_rate'].iloc[0]}, got {calculated_dir}"

if __name__ == "__main__":
    pytest.main()
