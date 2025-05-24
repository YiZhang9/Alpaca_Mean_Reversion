import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import math  # Import for rounding down to the nearest integer

import os

# Alpaca API 密钥和 Secret
API_KEY = os.getenv('PAPER_API_KEY')  # Use environment variables for security
API_SECRET = os.getenv('PAPER_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'  # 用于纸面交易（模拟账户）

# 创建 Alpaca API 实例
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# 创建 Alpaca Historical Data Client
client = StockHistoricalDataClient(API_KEY, API_SECRET)

# 股票池
world_1000_tickers = ['AAPL']  # Only using AAPL for now

initial_cash = 100000  
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}  
cash_history = []  # 用来记录现金余额的变化

def get_historical_data(ticker, moving_average_days):
    # 使用 Alpaca Historical API 获取历史数据
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Day,
        start='2020-01-01',  # Modify as per your requirement
        end='2023-12-31'
    )
    
    # Fetch the historical stock bars
    bars = client.get_stock_bars(request_params)
    
    # Ensure bars data is returned correctly
    if bars.df.empty:
        raise ValueError(f"No data found for {ticker}")
    
    # Create a DataFrame from the bars data
    stock_df = bars.df[['close']]  # Extract only 'close' column (since no timestamp)
    
    # Calculate the moving average
    stock_df[f'{moving_average_days}_MA'] = stock_df['close'].rolling(window=moving_average_days).mean()
    
    return stock_df

def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash):
    price_ratio = current_price / moving_avg

    if price_ratio <= 0.99:
        if price_ratio >= 0.85:
            buy_percentage = (1 - price_ratio) / (1 - 0.85)
        else:
            buy_percentage = 1

        amount_to_invest = allocation_per_stock * buy_percentage
        shares_to_buy = math.floor(amount_to_invest / current_price)  # Ensure we buy whole shares

        # Check if we have enough cash for this purchase
        if shares_to_buy > 0 and (shares_to_buy * current_price) <= cash:
            portfolio[ticker] += shares_to_buy
            cash -= shares_to_buy * current_price
            cash_history.append(cash)  # Record the new cash balance

            try:
                # Check actual buying power via Alpaca API
                account = api.get_account()
                if float(account.buying_power) >= shares_to_buy * current_price:
                    # Submit buy order through Alpaca
                    api.submit_order(
                        symbol=ticker,
                        qty=shares_to_buy,
                        side='buy',
                        type='market',
                        time_in_force='gtc'  # Good 'til cancelled
                    )
                else:
                    print(f"Insufficient buying power to purchase {shares_to_buy} shares of {ticker} at {current_price}.")
            except Exception as e:
                print(f"An error occurred while submitting the order: {e}")
        else:
            print(f"Not enough cash to purchase {shares_to_buy} shares of {ticker} at {current_price}.")
    
    return cash


def backtest_strategy(moving_average_days):
    cash = initial_cash
    cash_history.append(cash)  # Record initial cash
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days)
        for index, row in stock_data.iterrows():
            current_price = row['close']
            moving_avg = row[f'{moving_average_days}_MA']

            if pd.notna(moving_avg):  
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash)

            # Ensure there are enough shares to sell
            if current_price > moving_avg and portfolio[ticker] > 0:
                shares_to_sell = portfolio[ticker]
                
                # Ensure we are not selling more shares than we own
                if shares_to_sell > 0:
                    portfolio[ticker] = 0
                    cash += shares_to_sell * current_price
                    cash_history.append(cash)  # Record cash after selling

                    # Execute the sell order through Alpaca
                    try:
                        api.submit_order(
                            symbol=ticker,
                            qty=shares_to_sell,
                            side='sell',
                            type='market',
                            time_in_force='gtc'
                        )
                    except Exception as e:
                        print(f"An error occurred while submitting the sell order for {ticker}: {e}")
                else:
                    print(f"Attempting to sell more shares than available for {ticker}. Available: {portfolio[ticker]}, Trying to sell: {shares_to_sell}")
    
    return cash


def sell_all_positions(cash, moving_average_days):
    for ticker, shares in portfolio.items():
        if shares > 0:  # Only try to sell if there are shares in the portfolio
            current_price = get_historical_data(ticker, moving_average_days)['close'].iloc[-1]  # Get the latest price
            
            # Ensure we are not trying to sell more shares than we own
            if shares > 0:
                cash += shares * current_price  # Calculate the cash after selling the shares
                portfolio[ticker] = 0  # Set the portfolio to zero after selling
                cash_history.append(cash)  # Record the new cash balance

                try:
                    # Ensure the requested qty matches the shares available
                    api.submit_order(
                        symbol=ticker,
                        qty=shares,  # Only sell the shares we have
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                except Exception as e:
                    print(f"An error occurred while submitting the sell order for {ticker}: {e}")
            else:
                print(f"Trying to sell more shares than available for {ticker}. Available: {portfolio[ticker]}")
    return cash


def test_different_moving_averages():
    results = []
    for days in range(10, 40):  
        print(f"Testing with {days}-day moving average...")
        cash_history.clear()  # 每次测试前清空现金记录
        cash = backtest_strategy(days)
        remaining_cash = sell_all_positions(cash, days)
        results.append((days, remaining_cash))
        print(f"Final remaining cash with {days}-day MA: {remaining_cash}")

        # 将cash历史记录保存为文件
        cash_history_df = pd.DataFrame(cash_history, columns=['Cash Balance'])
        cash_history_df.to_csv(f'cash_history_{days}_days_MA.csv', index=False)
    
    print("\nResults for different moving average days:")
    for result in results:
        print(f"{result[0]}-day MA: {result[1]} remaining cash")
    
    df_results = pd.DataFrame(results, columns=['Moving Average Days', 'Remaining Cash'])
    df_results.to_csv('moving_average_test_results_run_1.csv', index=False)
    print("\nResults saved to 'moving_average_test_results_run_1.csv'.")

test_different_moving_averages()