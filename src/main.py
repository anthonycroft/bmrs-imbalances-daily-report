from datetime import datetime, timedelta

import pandas as pd
import requests

# calculate yesterday's date
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# endpoint for Indicative Imbalance Settlement
BMRS_API_ENDPOINT = f"https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/{yesterday}?format=json"


# Function to get system imbalance cost and price
def get_system_imbalance_data():
    # Calculate previous day (BMRS typically updates for previous day)

    # Make the GET request to retrieve the imbalance data
    response = requests.get(f"{BMRS_API_ENDPOINT}")

    # Check if request was successful
    if response.status_code == 200:
        # Parse the response
        data = response.json()

        # Load data into a pandas DataFrame
        df = pd.DataFrame(data["data"])[
            [
                "settlementDate",
                "settlementPeriod",
                "startTime",
                "systemSellPrice",
                "systemBuyPrice",
                "netImbalanceVolume",
            ]
        ]

        # Print the DataFrame for review
        print(df)

        # Return the DataFrame for further use
        return df

        # Print data points for review
        # for item in data["data"]:
        #     print(f"Settlement Date: {item['settlementDate']}")
        #     print(f"Settlement Period: {item['settlementPeriod']}")
        #     print(f"Start Time: {item['startTime']}")
        #     print(f"System Sell Price: {item['systemSellPrice']}")
        #     print(f"System Buy Price: {item['systemBuyPrice']}")
        #     print(f"Net Imbalance Volume: {item['netImbalanceVolume']}")
        #     print("---")
    else:
        print(f"Error: Unable to fetch data, Status code {response.status_code}")


if __name__ == "__main__":
    get_system_imbalance_data()
