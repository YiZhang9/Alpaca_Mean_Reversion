import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import os

# Alpaca API 密钥和 Secret
API_KEY = os.getenv('LIVE_API_KEY')  # Use environment variables for security
API_SECRET = os.getenv('LIVE_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'  # 用于纸面交易（模拟账户）

# 创建 Alpaca API 实例
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# 创建 Alpaca Historical Data Client
client = StockHistoricalDataClient(API_KEY, API_SECRET)

# 股票池
world_1000_tickers = ['AAPL']  # Test with a subset of tickers for simplicity
initial_cash = 100000
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}
cash_history = []

# Function to fetch historical data
def fetch_historical_data(ticker, start_date, end_date):
    """Fetch historical data for a specific ticker."""
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Day,
        start=start_date,
        end=end_date
    )
    bars = client.get_stock_bars(request_params)
    if bars.df.empty:
        raise ValueError(f"No data found for {ticker}")
    return bars.df

# Function to calculate moving average
def calculate_moving_average(data, column, window):
    """Calculate the moving average for a specified column."""
    data[f'{window}_MA'] = data[column].rolling(window=window).mean()
    return data

def buy_stock(ticker, current_price, moving_avg, cash, threshold=0.99, min_ratio=0.85):
    """Buy stock if the price is below the moving average by a threshold."""
    price_ratio = current_price / moving_avg
    if price_ratio <= threshold:
        buy_percentage = (1 - price_ratio) / (1 - min_ratio) if price_ratio >= min_ratio else 1
        amount_to_invest = allocation_per_stock * buy_percentage
        shares_to_buy = int(amount_to_invest // current_price)

        if shares_to_buy > 0:
            try:
                # Submit a buy order
                api.submit_order(
                    symbol=ticker,
                    qty=shares_to_buy,
                    side='buy',
                    type='market',
                    time_in_force='gtc'  # Good 'til cancelled
                )
                print(f"Submitted buy order for {shares_to_buy} shares of {ticker}.")
            except Exception as e:
                print(f"Failed to submit buy order for {ticker}: {e}")
        return shares_to_buy
    return 0


def sell_stock(ticker, current_price, shares):
    """Sell all shares of a stock."""
    if shares > 0:
        try:
            # Submit a sell order
            api.submit_order(
                symbol=ticker,
                qty=shares,
                side='sell',
                type='market',
                time_in_force='gtc'  # Good 'til cancelled
            )
            print(f"Submitted sell order for {shares} shares of {ticker}.")
        except Exception as e:
            print(f"Failed to submit sell order for {ticker}: {e}")
    return shares * current_price

# Backtest function
def backtest(tickers, moving_avg_days, start_date, end_date):
    cash = initial_cash
    for ticker in tickers:
        try:
            df = fetch_historical_data(ticker, start_date, end_date)
            df = calculate_moving_average(df, 'close', moving_avg_days)
            for _, row in df.iterrows():
                if pd.notna(row[f'{moving_avg_days}_MA']):
                    shares_to_buy = buy_stock(
                        ticker, row['close'], row[f'{moving_avg_days}_MA'], cash
                    )
                    cash -= shares_to_buy * row['close']
                    portfolio[ticker] += shares_to_buy

                    if row['close'] > row[f'{moving_avg_days}_MA'] and portfolio[ticker] > 0:
                        cash += sell_stock(ticker, row['close'], portfolio[ticker])
                        portfolio[ticker] = 0
        except Exception as e:
            print(f"Error with {ticker}: {e}")
    return cash

def sell_all_positions(cash, moving_avg_days):
    for ticker, shares in portfolio.items():
        if shares > 0:
            try:
                # Get the latest price for the ticker
                current_price = fetch_historical_data(ticker, "2023-12-01", "2023-12-31")['close'].iloc[-1]
                # Submit a sell order
                api.submit_order(
                    symbol=ticker,
                    qty=shares,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
                print(f"Submitted sell order for {shares} shares of {ticker}.")
                cash += shares * current_price
                portfolio[ticker] = 0
                cash_history.append(cash)
            except Exception as e:
                print(f"Failed to sell all positions for {ticker}: {e}")
    return cash


# Test with a specific moving average day
def test_specific_day(moving_avg_days, tickers, start_date, end_date):
    print(f"Testing with {moving_avg_days}-day moving average...")
    cash_history.clear()
    remaining_cash = backtest(tickers, moving_avg_days, start_date, end_date)
    remaining_cash = sell_all_positions(remaining_cash, moving_avg_days)
    
    # Save results
    cash_history_df = pd.DataFrame(cash_history, columns=['Cash Balance'])
    cash_history_df.to_csv(f'cash_history_{moving_avg_days}_days_MA.csv', index=False)
    print(f"\nFinal remaining cash with {moving_avg_days}-day MA: {remaining_cash}")
    result = [(moving_avg_days, remaining_cash)]
    df_result = pd.DataFrame(result, columns=['Moving Average Days', 'Remaining Cash'])
    df_result.to_csv(f'moving_average_test_results_{moving_avg_days}_days.csv', index=False)
    print(f"\nResult saved to 'moving_average_test_results_{moving_avg_days}_days.csv'.")

# Parameters for testing
specific_day = 40  # Moving average days
start_date = "2020-01-01"
end_date = "2023-12-31"

# Run the test
test_specific_day(specific_day, world_1000_tickers, start_date, end_date)
