import requests
import pandas as pd
from datetime import datetime

# List of coins and their Binance symbols
coins = {
    "BTCUSDT": "BTC",
    "ETHUSDT": "ETH",
    "BNBUSDT": "BNB",
    "USDTUSDT": "USDT",
    "SOLUSDT": "SOL",
    "USDCUSDT": "USDC"
}

# Base URL for Binance API
base_url = "https://api.binance.com/api/v3/klines"

# Define the time interval and other parameters
interval = "1d"  # Daily data
start_time = int(datetime(2024, 1, 1).timestamp() * 1000)  # Start date
end_time = int(datetime(2024, 8, 20).timestamp() * 1000)  # End date

# Function to fetch and process data
def get_historical_data(symbol, coin_name):
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time,
        "limit": 1000  # Maximum number of records per request
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=[
        "Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
        "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
        "Taker Buy Quote Asset Volume", "Ignore"
    ])

    # Format and select the required columns
    df['Date'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Name'] = coin_name
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Name']]

    return df

# Fetch and combine data for all specified coins
combined_data = pd.concat([get_historical_data(symbol, name) for symbol, name in coins.items()])

# Reset index for the combined DataFrame
combined_data.reset_index(drop=True, inplace=True)

# Display the first few rows of the combined data
print(combined_data.head())

# Optionally, save the data to a CSV file, appending new data
file_path = "binance_historical_data.csv"

# Check if file exists to determine the mode
if pd.io.common.file_exists(file_path):
    # If file exists, append new data
    combined_data.to_csv(file_path, mode='a', header=False, index=False)
else:
    # If file does not exist, write new file
    combined_data.to_csv(file_path, index=False)