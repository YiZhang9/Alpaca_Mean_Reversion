import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

world_1000_tickers = ['CVCO', 'NVCR', 'FNLC', 'NVEC', 'UONEK', 'STRT', 'CEAD', 'SLAB', 'AXON', 'AGNC', 'SCOR', 'STRR', 'STRS', 'SCNX', 'SCNI', 'CMRX']

initial_cash = 10000  
portfolio = {ticker: 0 for ticker in world_1000_tickers}  

# 获取公司当前的已发行股票数量
def get_shares_outstanding(ticker):
    stock_info = yf.Ticker(ticker).info
    return stock_info.get('sharesOutstanding', 0)  # 如果找不到数据，返回0

# 获取实时市值数据（基于历史股价和股票数量）
def get_historical_market_cap(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    shares_outstanding = get_shares_outstanding(ticker)  # 使用当前股票数量作为近似值
    stock_data['Market Cap'] = stock_data['Close'] * shares_outstanding  # 市值 = 收盘价 * 股票数量
    return stock_data

# 按实时市值倒数分配资金（市值越小分配的资金越多），没有市值的公司也分配资金
def allocate_funds_by_inverse_market_cap(tickers, start_date, end_date, initial_cash, min_allocation=0.05):
    market_caps = {}
    
    for ticker in tickers:
        stock_data = get_historical_market_cap(ticker, start_date, end_date)
        total_market_cap = stock_data['Market Cap'].sum()  # 求总市值作为分配基础
        market_caps[ticker] = total_market_cap  # 保存该公司的总市值
    
    # 计算市场资本的倒数，确保市值为0的公司仍然获得分配
    inverse_market_caps = {ticker: 1 / market_caps[ticker] if market_caps[ticker] > 0 else min_allocation for ticker in tickers}
    total_inverse_market_cap = sum(inverse_market_caps.values())  # 计算所有公司的总倒数市值
    
    allocation = {}
    for ticker in tickers:
        allocation[ticker] = (inverse_market_caps[ticker] / total_inverse_market_cap) * initial_cash  # 根据倒数市值分配资金
    return allocation

# 获取历史数据
def get_historical_data(ticker, moving_average_days, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    stock_data[f'{moving_average_days}_MA'] = stock_data['Close'].rolling(window=moving_average_days).mean()  
    return stock_data

# 买入操作：只要股价低于移动均线的95%就买入
def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash, allocation_per_stock):
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
    
    return cash

# 回测交易策略
def backtest_strategy(moving_average_days, allocation, start_date, end_date):
    cash = initial_cash
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days, start_date, end_date)
        allocation_per_stock = allocation[ticker]  # 使用按市值分配的资金
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg = row[f'{moving_average_days}_MA']

            if pd.notna(moving_avg):  
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash, allocation_per_stock)

            if current_price > moving_avg * 1 and portfolio[ticker] > 0:
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
    
    return cash

# 清算所有持仓
def sell_all_positions(cash, moving_average_days, start_date, end_date):
    for ticker, shares in portfolio.items():
        if shares > 0:  
            current_price = get_historical_data(ticker, moving_average_days, start_date, end_date)['Close'].iloc[-1]  
            cash += shares * current_price  
            portfolio[ticker] = 0  
    return cash

# 测试不同的均线天数
def test_different_moving_averages():
    start_date = "2000-01-01"
    end_date = "2023-01-01"
    
    # 按实时市值倒数分配初始资金，没有市值数据的公司也分配资金
    allocation = allocate_funds_by_inverse_market_cap(world_1000_tickers, start_date, end_date, initial_cash, min_allocation=0.05)
    
    results = []
    for days in range(1310, 1330):  
        print(f"Testing with {days}-day moving average...")
        cash = backtest_strategy(days, allocation, start_date, end_date)
        remaining_cash = sell_all_positions(cash, days, start_date, end_date)
        results.append((days, remaining_cash))
        print(f"Final remaining cash with {days}-day MA: {remaining_cash}")
    
    print("\nResults for different moving average days:")
    for result in results:
        print(f"{result[0]}-day MA: {result[1]} remaining cash")
    
    df_results = pd.DataFrame(results, columns=['Moving Average Days', 'Remaining Cash'])
    
    df_results.to_csv('moving_average_test_results_inverse_market_cap_with_min_allocation.csv', index=False)
    print("\nResults saved to 'moving_average_test_results_inverse_market_cap_with_min_allocation.csv'.")

test_different_moving_averages()
