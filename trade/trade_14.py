import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

world_1000_tickers = ['CVCO', 'NVCR', 'FNLC', 'NVEC', 'UONEK', 'STRT', 'CEAD', 'SLAB', 'AXON', 'AGNC', 'SCOR', 'STRR', 'STRS', 'SCNX', 'SCNI', 'CMRX']

initial_cash = 10000  
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: {'shares': 0, 'invested_amount': 0} for ticker in world_1000_tickers}  # 新增 invested_amount 记录每只股票的已投资金额

def get_historical_data(ticker, moving_average_days):
    stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
    stock_data[f'{moving_average_days}_MA'] = stock_data['Close'].rolling(window=moving_average_days).mean()  
    return stock_data

def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash):
    price_ratio = current_price / moving_avg

    if price_ratio <= 0.95:
        if price_ratio >= 0.85:
            buy_percentage = (0.95 - price_ratio) / (0.95 - 0.85)  
        else:
            buy_percentage = 1

        amount_to_invest = allocation_per_stock * buy_percentage
        remaining_allocation = allocation_per_stock - portfolio[ticker]['invested_amount']  # 剩余可投资的资金

        if remaining_allocation > 0:
            # 只购买剩余分配资金以内的股票
            amount_to_invest = min(amount_to_invest, remaining_allocation)  
            shares_to_buy = amount_to_invest // current_price  

            if shares_to_buy > 0:
                portfolio[ticker]['shares'] += shares_to_buy
                portfolio[ticker]['invested_amount'] += shares_to_buy * current_price  # 更新已投资金额
                cash -= shares_to_buy * current_price
    
    return cash

def sell_stock_if_above_threshold(ticker, current_price, moving_avg, cash):
    price_ratio = current_price / moving_avg
    if price_ratio > 0.95 and portfolio[ticker]['shares'] > 0:
        # 随着价格上涨，逐步卖出
        if price_ratio < 1.0:
            sell_percentage = (price_ratio - 0.95) / (1.0 - 0.95)
        else:
            sell_percentage = 1

        shares_to_sell = int(portfolio[ticker]['shares'] * sell_percentage)
        
        if shares_to_sell > 0:
            portfolio[ticker]['shares'] -= shares_to_sell
            portfolio[ticker]['invested_amount'] -= shares_to_sell * current_price  # 减去对应投资的金额
            cash += shares_to_sell * current_price  # 卖出的现金回流

    return cash

def backtest_strategy(moving_average_days):
    cash = initial_cash
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days)
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg = row[f'{moving_average_days}_MA']

            if pd.notna(moving_avg):  
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash)
                cash = sell_stock_if_above_threshold(ticker, current_price, moving_avg, cash)  # 卖出操作

    return cash

def sell_all_positions(cash, moving_average_days):
    for ticker, data in portfolio.items():
        if data['shares'] > 0:  
            current_price = get_historical_data(ticker, moving_average_days)['Close'].iloc[-1]  
            cash += data['shares'] * current_price  
            portfolio[ticker]['shares'] = 0  
            portfolio[ticker]['invested_amount'] = 0  # 清空投资金额
    return cash

def test_different_moving_averages():
    results = []
    for days in range(1000, 1010):  
        print(f"Testing with {days}-day moving average...")
        cash = backtest_strategy(days)
        remaining_cash = sell_all_positions(cash, days)
        results.append((days, remaining_cash))
        print(f"Final remaining cash with {days}-day MA: {remaining_cash}")
    
    print("\nResults for different moving average days:")
    for result in results:
        print(f"{result[0]}-day MA: {result[1]} remaining cash")
    
    df_results = pd.DataFrame(results, columns=['Moving Average Days', 'Remaining Cash'])
    
    df_results.to_csv('moving_average_test_results_14.csv', index=False)
    print("\nResults saved to 'moving_average_test_results_14.csv'.")

test_different_moving_averages()
