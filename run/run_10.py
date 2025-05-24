import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import os

# Alpaca API Keys and Secret
API_KEY = os.getenv('LIVE_API_KEY')  # Use environment variables for security
API_SECRET = os.getenv('LIVE_API_SECRET')
BASE_URL = 'https://api.alpaca.markets'  # For live trading

# Create Alpaca API and Historical Data Client
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')
client = StockHistoricalDataClient(API_KEY, API_SECRET)

# Stock pool
world_1000_tickers = ['AAPL']  # Example subset of tickers
portfolio = {ticker: 0 for ticker in world_1000_tickers}  # Initialize portfolio
cash_history = []  # Track cash changes

# Function to fetch historical data
def fetch_historical_data(ticker, moving_avg_days):
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Day,
        start=None,  # Default to fetching up to the latest date
        limit=moving_avg_days  # Fetch only the past `moving_avg_days`
    )
    bars = client.get_stock_bars(request_params)
    if bars.df.empty:
        raise ValueError(f"No data found for {ticker}")
    return bars.df

# Function to calculate moving average
def calculate_moving_average(data, column, window):
    data[f'{window}_MA'] = data[column].rolling(window=window).mean()
    return data

# Function to get buying power
def get_buying_power():
    account = api.get_account()
    return float(account.buying_power)

# Function to buy stock
def buy_stock(ticker, current_price, moving_avg, buying_power, threshold=0.99, min_ratio=0.85):
    price_ratio = current_price / moving_avg
    if price_ratio <= threshold:
        buy_percentage = (1 - price_ratio) / (1 - min_ratio) if price_ratio >= min_ratio else 1
        amount_to_invest = min(buying_power, buy_percentage * current_price)
        shares_to_buy = int(amount_to_invest // current_price)
        if shares_to_buy > 0:
            try:
                api.submit_order(
                    symbol=ticker,
                    qty=shares_to_buy,
                    side='buy',
                    type='market',
                    time_in_force='gtc'
                )
                print(f"Submitted buy order for {shares_to_buy} shares of {ticker}.")
                return shares_to_buy
            except Exception as e:
                print(f"Failed to submit buy order for {ticker}: {e}")
    return 0

# Function to sell stock
def sell_stock(ticker, current_price, shares):
    try:
        api.submit_order(
            symbol=ticker,
            qty=shares,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        print(f"Submitted sell order for {shares} shares of {ticker}.")
        return shares * current_price
    except Exception as e:
        print(f"Failed to submit sell order for {ticker}: {e}")
        return 0

# Live trading function
def live_trading(tickers, moving_avg_days):
    while True:  # Continuous live trading loop
        try:
            for ticker in tickers:
                print(f"Processing {ticker}...")
                buying_power = get_buying_power()
                print(f"Buying power: {buying_power}")

                # Fetch historical data
                historical_data = fetch_historical_data(ticker, moving_avg_days)
                historical_data = calculate_moving_average(historical_data, 'close', moving_avg_days)
                current_price = historical_data['close'].iloc[-1]
                moving_avg = historical_data[f'{moving_avg_days}_MA'].iloc[-1]

                # Attempt to buy stock
                shares_to_buy = buy_stock(ticker, current_price, moving_avg, buying_power)
                portfolio[ticker] += shares_to_buy

                # Check sell condition
                if current_price > moving_avg and portfolio[ticker] > 0:
                    cash = sell_stock(ticker, current_price, portfolio[ticker])
                    portfolio[ticker] = 0
        except Exception as e:
            print(f"Error with {ticker}: {e}")

# Parameters
moving_avg_days = 40  # Moving average days

# Run live trading
live_trading(world_1000_tickers, moving_avg_days)
