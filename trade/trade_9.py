import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

world_1000_tickers = ['CVCO', 'NVCR', 'FNLC', 'NVEC', 'UONEK', 'STRT', 'CEAD', 'SLAB', 'AXON', 'AGNC', 'SCOR', 'STRR', 'STRS', 'SCNX', 'SCNI', 'CMRX']

initial_cash = 10000  
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}  
cash_history = []  # 新增变量，用来记录现金余额的变化

def get_historical_data(ticker, moving_average_days):
    stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
    stock_data[f'{moving_average_days}_MA'] = stock_data['Close'].rolling(window=moving_average_days).mean()  
    return stock_data

def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash):
    price_ratio = current_price / moving_avg

    if price_ratio <= 0.99:
        if price_ratio >= 0.85:
            buy_percentage = (1 - price_ratio) / (1 - 0.85)  
        else:
            buy_percentage = 1

        amount_to_invest = allocation_per_stock * buy_percentage
        shares_to_buy = amount_to_invest // current_price  

        if shares_to_buy > 0:
            portfolio[ticker] += shares_to_buy
            cash -= shares_to_buy * current_price
            cash_history.append(cash)  # 记录买入后的现金余额
    
    return cash

def backtest_strategy(moving_average_days):
    cash = initial_cash
    cash_history.append(cash)  # 记录初始现金
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days)
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg = row[f'{moving_average_days}_MA']

            if pd.notna(moving_avg):  
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash)

            if current_price > moving_avg * 1 and portfolio[ticker] > 0:
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                cash_history.append(cash)  # 记录卖出后的现金余额
    
    return cash

def sell_all_positions(cash, moving_average_days):
    for ticker, shares in portfolio.items():
        if shares > 0:  
            current_price = get_historical_data(ticker, moving_average_days)['Close'].iloc[-1]  
            cash += shares * current_price  
            portfolio[ticker] = 0  
            cash_history.append(cash)  # 记录卖出后的现金余额
    return cash

def test_different_moving_averages():
    results = []
    for days in range(1310,1330):  
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
    
    df_results.to_csv('moving_average_test_results_9.csv', index=False)
    print("\nResults saved to 'moving_average_test_results_9.csv'.")

test_different_moving_averages()
