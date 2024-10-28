from . import calculations as ca

from pandas import DataFrame

def print_report(nic: float, dir: float) -> None:
   
    # Print summary report
    print(f"Total Daily Imbalance Cost: £{nic:,.0f}")
    print(f"Daily Imbalance Unit Rate: £{dir:,.2f} per MWh")

def create_imbalance_report(df: DataFrame) -> None:
    ca.create_calculated_columns(df)
    nic = ca.net_imbalance_cost_total(df)
    dir = ca.daily_imbalance_unit_rate(df)
    print_report(nic, dir)