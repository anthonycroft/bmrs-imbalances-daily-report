BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/balancing/settlement/system-prices/"

EXPECTED_TYPES = {
    "settlementDate": "datetime64[ns]",
    "settlementPeriod": "int64",
    "startTime": "datetime64[ns, UTC]",
    "systemSellPrice": "float64",
    "systemBuyPrice": "float64",
    "netImbalanceVolume": "float64",
}

# Columns used in the project
REQUIRED_COLUMNS_RENAMER = {
    "settlementDate": "date",
    "startTime": "startTime",
    "systemSellPrice": "price",
    "netImbalanceVolume": "volume",
}

