import yfinance as yf
import pandas as pd

# Fortune 500 企业列表（假设一些常见的公司）
world_500_tickers = ['CVCO', 'NMRK', 'NVEI', 'OPTN', 'NVCR', 'ZPTA', 'FNKO', 'NVCT', 'FNLC', 'NVEC', 'TWST', 'BSBK', 'UONEK', 'STRT', 'CEAD', 'NMRA', 'SLAB', 'BCG', 'AXON', 'OPTX', 'AGNC', 'SCOR', 'STRR', 'IFRX', 'STRS', 'KLXE', 'SCNX', 'SCNI', 'CMRX', 'SDA']

# 初始资金分为10份
initial_cash = 100000  # 假设初始资金为10万美元
allocation_per_stock = initial_cash / len(world_500_tickers)
portfolio = {ticker: 0 for ticker in world_500_tickers}  # 初始持仓为空

# 获取从2000年开始的历史数据
def get_historical_data(ticker):
    stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
    stock_data['20_MA'] = stock_data['Close'].rolling(window=20).mean()  # 计算20日均线
    return stock_data

# 回测交易策略
def backtest_strategy():
    cash = initial_cash
    for ticker in world_500_tickers:
        stock_data = get_historical_data(ticker)
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg_20 = row['20_MA']

            # 条件1: 如果价格低于20日均线的92%，买入
            if current_price < moving_avg_20 * 0.92:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            # 条件2: 如果价格涨回到20日均线的95%，卖出
            elif current_price > moving_avg_20 * 0.95 and portfolio[ticker] > 0:  # 持仓时卖出
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                print(f"Sold {shares_to_sell} shares of {ticker} at {current_price} on {index}")

    print(f"Final portfolio: {portfolio}")
    print(f"Remaining cash: {cash}")

# 运行回测策略
backtest_strategy()
