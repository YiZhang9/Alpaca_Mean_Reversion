import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import pandas as pd
import os

# Alpaca API keys
API_KEY = os.getenv('PAPER_API_KEY')  # Replace with your API key
API_SECRET = os.getenv('PAPER_API_SECRET')  # Replace with your API secret
BASE_URL = 'https://paper-api.alpaca.markets'  # Paper trading base URL

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

def fetch_historical_data(ticker, days):
    """Fetch historical data for the last `days`."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    try:
        bars = api.get_bars(
            ticker,
            timeframe="1Day",
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d'),
            feed="iex"  # Use IEX data feed
        )
        if not bars:
            raise ValueError(f"No data found for ticker: {ticker}")

        df = pd.DataFrame([{'timestamp': bar.t, 'close': bar.c} for bar in bars])
        return df
    except Exception as e:
        raise ValueError(f"Failed to fetch data for {ticker}: {e}")

def calculate_average_price(data):
    """Calculate the average price from historical data."""
    return data['close'].mean()

# Main function
def calculate_price_ratio(ticker):
    try:
        # Fetch historical data for the last 1310 days
        historical_data = fetch_historical_data(ticker, 1310)

        # Calculate the 1310-day average price
        avg_price = calculate_average_price(historical_data)

        # Fetch the latest price
        latest_price = historical_data['close'].iloc[-1]

        # Calculate the percentage of the current price relative to the average
        percentage = (latest_price / avg_price) * 100

        # Print the result
        print(f"Ticker: {ticker}")
        print(f"1310-day average price: {avg_price:.2f}")
        print(f"Current price: {latest_price:.2f}")
        print(f"Current price is {percentage:.2f}% of the 1310-day average price.")
    except Exception as e:
        print(f"Error for {ticker}: {e}")

# Example usage
ticker = "AAPL"  # Replace with your desired ticker symbol
calculate_price_ratio(ticker)
