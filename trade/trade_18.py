import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta
import os

# Alpaca API credentials
API_KEY = os.getenv('PAPER_API_KEY')  # Use environment variables for security
API_SECRET = os.getenv('PAPER_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'  # For paper trading accounts

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version="v2")

# Parameters
symbol = "AAPL"  # Replace with the desired stock symbol
days = 1300

# Fetch historical data for the past 1300 days
end_date = datetime.now()
start_date = end_date - timedelta(days=days)

data = api.get_bars(symbol, "day", start=start_date.isoformat(), end=end_date.isoformat())[symbol]

# Convert to DataFrame for easier processing
prices = pd.DataFrame([{"date": bar.t, "close": bar.c} for bar in data])

# Calculate the average price over the past 1300 days
average_price = prices["close"].mean()

# Get the latest price
current_price = prices.iloc[-1]["close"]

# Calculate the ratio of current price to the 1300-day average price
price_ratio = current_price / average_price

# Display the results
print(f"Symbol: {symbol}")
print(f"Average price over the past {days} days: {average_price:.2f}")
print(f"Current price: {current_price:.2f}")
print(f"Ratio (Current Price / 1300-day Average): {price_ratio:.2f}")
