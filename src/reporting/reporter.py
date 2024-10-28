from . import calculations as ca

from pandas import DataFrame

"""
Creates the final output Report and vsiualisation (uses Dash for this purpose)
"""

def print_report(nic: float, dir: float, date: str, hour: str, volume: float) -> None:
   
    # Print summary report
    print()
    print("----------------------")
    print("Daily Imbalance Report")
    print("======================")
    print()
    print(f"Total Daily Imbalance Cost: £{nic:,.0f}")
    print(f"Daily Imbalance Unit Rate: £{dir:,.2f} per MWh")
    # print(f"Hour with highest absolute imbalance volume: £{hour}")
    print()
    # Print the result in a nicely formatted string
    print("Highest absolute imbalance volume:\n")
    print(f"Date: {date}\nHour: {hour}\nVolume: {volume:.2f} MWh")
    print()
    print("----------------------")
    print()

def create_imbalance_report(df: DataFrame) -> None:
    ca.create_calculated_columns(df)
    nic = ca.net_imbalance_cost_total(df)
    dir = ca.daily_imbalance_unit_rate(df)

    # Calculate the row with the maximum absolute imbalance volume
    max_row = ca.calculate_hour(df)

    # Extract the relevant details for formatted output
    date = max_row["date"].strftime("%d-%m-%Y")
    hour = max_row["hour"].strftime("%H:%M")  # Format the hour if needed
    volume = max_row["absoluteVolume"]  
    print_report(nic, dir, date, hour, volume)