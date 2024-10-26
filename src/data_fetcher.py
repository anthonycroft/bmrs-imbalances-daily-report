from datetime import datetime, timedelta
import pandas as pd
import requests

class ImbalanceDataFetcher:
    """Fetches imbalance data from the Elexon API."""

    BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/"
    EXPECTED_TYPES = {
        "settlementDate": "datetime64[ns]",
        "settlementPeriod": "int64",
        "startTime": "datetime64[ns, UTC]",
        "systemSellPrice": "float64",
        "systemBuyPrice": "float64",
        "netImbalanceVolume": "float64",
    }

    def __init__(self, date: str = None):
        self.date = date or (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    def fetch_data(self) -> pd.DataFrame:
        """Fetches imbalance data from the Elexon API."""
        
        endpoint = f"{self.BASE_URL}{self.date}?format=json"
        response = requests.get(endpoint)

        # deal with response errors
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data["data"])[list(self.EXPECTED_TYPES.keys())]
            return self.enforce_data_types(df)
        else:
            raise ValueError(f"Error fetching data, status code {response.status_code}")

    def enforce_data_types(self, df: pd.DataFrame) -> pd.DataFrame:
        for column, expected_type in self.EXPECTED_TYPES.items():
            try:
                df[column] = df[column].astype(expected_type)
            except ValueError as e:
                raise ValueError(f"Column '{column}' could not be cast to {expected_type}. Error: {e}")
        return df

