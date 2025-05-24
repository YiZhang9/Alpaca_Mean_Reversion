import alpaca_trade_api as tradeapi
import pandas as pd
from datetime import datetime, timedelta
import os

# Alpaca API keys
API_KEY = os.getenv('LIVE_API_KEY')  # Use environment variables for security
API_SECRET = os.getenv('LIVE_API_SECRET')
BASE_URL = 'https://api.alpaca.markets'  # Live trading URL

# Initialize Alpaca API
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# Portfolio and initial setup
portfolio = {}
moving_avg_days = 40

def fetch_historical_data(ticker):
    """Fetch historical data for the past 40 days using IEX data source."""
    end_date = datetime.now().date()  # Today's date
    start_date = end_date - timedelta(days=moving_avg_days * 2)  # Extra buffer for weekends/holidays

    try:
        barset = api.get_bars(
            ticker,
            timeframe="1Day",
            start=start_date.isoformat(),
            end=end_date.isoformat(),
            feed='iex'  # Force IEX feed for free data
        )
        if not barset:
            raise ValueError(f"No data available for ticker: {ticker}")

        df = pd.DataFrame([{
            'timestamp': bar.t,
            'close': bar.c
        } for bar in barset])
        
        # Calculate moving average
        df['moving_avg'] = df['close'].rolling(window=moving_avg_days).mean()
        return df
    except Exception as e:
        raise ValueError(f"Failed to fetch historical data for {ticker}: {e}")


# Buy stock if current price is below 95% of the moving average
def buy_stock(ticker, current_price, moving_avg):
    global portfolio
    if current_price < 0.95 * moving_avg:
        cash = float(api.get_account().cash)
        shares_to_buy = int(cash // current_price)
        if shares_to_buy > 0:
            api.submit_order(
                symbol=ticker,
                qty=shares_to_buy,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            portfolio[ticker] = portfolio.get(ticker, 0) + shares_to_buy
            print(f"Bought {shares_to_buy} shares of {ticker} at {current_price}")
        else:
            print(f"Insufficient cash to buy {ticker}.")

# Sell stock if current price exceeds the moving average
def sell_stock(ticker, current_price, moving_avg):
    global portfolio
    if current_price > moving_avg and portfolio.get(ticker, 0) > 0:
        shares_to_sell = portfolio[ticker]
        api.submit_order(
            symbol=ticker,
            qty=shares_to_sell,
            side='sell',
            type='market',
            time_in_force='gtc'
        )
        portfolio[ticker] = 0
        print(f"Sold {shares_to_sell} shares of {ticker} at {current_price}")

# Main live trading function
def live_trading(ticker):
    try:
        historical_data = fetch_historical_data(ticker)
        latest_data = historical_data.iloc[-1]
        current_price = latest_data['close']
        moving_avg = latest_data['moving_avg']

        if pd.notna(moving_avg):
            buy_stock(ticker, current_price, moving_avg)
            sell_stock(ticker, current_price, moving_avg)
        else:
            print(f"Not enough data to calculate moving average for {ticker}.")
    except Exception as e:
        print(f"Error for {ticker}: {e}")

# Example usage
ticker = 'AAPL'  # Replace with the ticker you want to trade
live_trading(ticker)
