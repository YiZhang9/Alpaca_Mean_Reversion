import yfinance as yf
import pandas as pd
import numpy as np

# Fortune 1000 企业列表（假设一些常见的公司）
world_1000_tickers = ['CVCO', 'NVCR', 'FNLC', 'NVEC', 'UONEK', 'STRT', 'CEAD', 'SLAB', 'AXON', 'AGNC', 'SCOR', 'STRR', 'STRS', 'SCNX', 'SCNI', 'CMRX']

initial_cash = 10000  # 总资金池
portfolio = {ticker: 0 for ticker in world_1000_tickers}  # 初始持仓为空

# 获取历史数据并计算指定天数的移动均线
def get_historical_data(ticker, moving_average_days):
    stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
    stock_data[f'{moving_average_days}_MA'] = stock_data['Close'].rolling(window=moving_average_days).mean()  # 动态计算均线
    return stock_data

# 买入操作：根据下跌幅度动态分配买入资金
def buy_stocks(all_data, date, cash, moving_average_days):
    drop_ratios = {}
    total_drop_percentage = 0

    for ticker, data in all_data.items():
        if date in data.index:  # 确保当前日期在数据集中
            price = data.loc[date, 'Close']
            moving_avg = data.loc[date, f'{moving_average_days}_MA']

            if pd.notna(moving_avg) and pd.notna(price) and price < moving_avg:  # 确保均线和价格都存在
                drop_ratio = (moving_avg - price) / moving_avg
                drop_ratios[ticker] = drop_ratio
                total_drop_percentage += drop_ratio

    if total_drop_percentage > 0:  # 确保至少有一家公司下跌
        for ticker, drop_ratio in drop_ratios.items():
            buy_percentage = drop_ratio / total_drop_percentage  # 计算买入比例
            price = all_data[ticker].loc[date, 'Close']  # 确保再次获取价格
            amount_to_invest = cash * buy_percentage
            shares_to_buy = amount_to_invest // price

            if shares_to_buy > 0:
                portfolio[ticker] += shares_to_buy
                cash -= shares_to_buy * price  # 扣除现金

    return cash

def backtest_strategy(moving_average_days):
    cash = initial_cash
    all_data = {ticker: get_historical_data(ticker, moving_average_days) for ticker in world_1000_tickers}  # 获取所有股票的数据
    dates = all_data[world_1000_tickers[0]].index  # 使用第一个股票的日期作为参考

    for date in dates:
        cash = buy_stocks(all_data, date, cash, moving_average_days)  # 每个日期检查是否买入

        for ticker in world_1000_tickers:
            if date in all_data[ticker].index:  # 确保该日期存在于该股票的数据集中
                price = all_data[ticker].loc[date, 'Close']
                moving_avg = all_data[ticker].loc[date, f'{moving_average_days}_MA']

                if pd.notna(moving_avg) and pd.notna(price) and price > moving_avg and portfolio[ticker] > 0:
                    shares_to_sell = portfolio[ticker]
                    portfolio[ticker] = 0
                    cash += shares_to_sell * price  # 卖出获得现金

    return cash

# 清算所有持仓
def sell_all_positions(cash, moving_average_days):
    for ticker, shares in portfolio.items():
        if shares > 0:  # 如果有持仓
            current_price = get_historical_data(ticker, moving_average_days)['Close'].iloc[-1]  # 获取最后一天的价格
            cash += shares * current_price  # 将股票市值转化为现金
            portfolio[ticker] = 0  # 清空持仓
    return cash

# 测试不同的均线天数
def test_different_moving_averages():
    results = []
    for days in range(1310, 1320):  # 例如，测试从50天到200天的均线
        print(f"Testing with {days}-day moving average...")
        cash = backtest_strategy(days)
        remaining_cash = sell_all_positions(cash, days)
        results.append((days, remaining_cash))
        print(f"Final remaining cash with {days}-day MA: {remaining_cash}")
    
    print("\nResults for different moving average days:")
    for result in results:
        print(f"{result[0]}-day MA: {result[1]} remaining cash")
    
    df_results = pd.DataFrame(results, columns=['Moving Average Days', 'Remaining Cash'])
    df_results.to_csv('moving_average_test_results.csv', index=False)
    print("\nResults saved to 'moving_average_test_results.csv'.")

# 运行测试
test_different_moving_averages()
