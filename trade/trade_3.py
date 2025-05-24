import yfinance as yf
import pandas as pd

# Fortune 1100 企业列表（假设一些常见的公司）
world_1100_tickers = ['CVCO', 'NMRK', 'NVEI', 'OPTN', 'NVCR', 'ZPTA', 'FNKO', 'NVCT', 'FNLC', 'NVEC', 'TWST', 'BSBK', 'UONEK', 'STRT', 'CEAD', 'NMRA', 'SLAB', 'BCG', 'AXON', 'OPTX', 'AGNC', 'SCOR', 'STRR', 'IFRX', 'STRS', 'KLXE', 'SCNX', 'SCNI', 'CMRX', 'SDA']
# world_1100_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'JPM', 'V', 'JNJ', 'NVDA']

# 初始资金分为10份
initial_cash = 11000  # 假设初始资金为10万美元
allocation_per_stock = initial_cash / len(world_1100_tickers)
portfolio = {ticker: 0 for ticker in world_1100_tickers}  # 初始持仓为空

# 获取从11000年开始的历史数据
def get_historical_data(ticker):
    stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
    stock_data['110_MA'] = stock_data['Close'].rolling(window=110).mean()  # 计算110日均线
    return stock_data



# 回测交易策略
def backtest_strategy():
    cash = initial_cash
    for ticker in world_1100_tickers:
        stock_data = get_historical_data(ticker)
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg_110 = row['110_MA']

            if current_price < moving_avg_110 * 0.94:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.93:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")


            if current_price < moving_avg_110 * 0.92:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")


            if current_price < moving_avg_110 * 0.91:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")


            if current_price < moving_avg_110 * 0.90:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")


            if current_price < moving_avg_110 * 0.89:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")


            if current_price < moving_avg_110 * 0.88:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")


            if current_price < moving_avg_110 * 0.87:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")



            if current_price < moving_avg_110 * 0.86:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.85:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.84:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")        

            # 条件1: 如果价格低于110日均线的92%，买入
            if current_price < moving_avg_110 * 0.83:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.82:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.81:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.80:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.79:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.78:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.77:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.76:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.75:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg_110 * 0.74:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            # 条件2: 如果价格涨回到20日均线的95%，卖出
            elif current_price > moving_avg_110 * 0.96 and portfolio[ticker] > 0:  # 持仓时卖出
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                # print(f"Sold {shares_to_sell} shares of {ticker} at {current_price} on {index}")
    
    # print(f"Final portfolio: {portfolio}")
    # print(f"Remaining cash: {cash}")
    return cash

def sell_all_positions(cash):
    for ticker, shares in portfolio.items():
        if shares > 0:  # 如果有持仓
            current_price = get_historical_data(ticker)['Close'].iloc[-1]  # 获取最后一天的价格
            cash += shares * current_price  # 将股票市值转化为现金
            print(f"Sold {shares} shares of {ticker} at {current_price} (final sell-off)")
            portfolio[ticker] = 0  # 清空持仓
    return cash

# 运行回测策略
cash = backtest_strategy()
remaining_cash = sell_all_positions(cash)
print(f"Final portfolio: {portfolio}")
print(f"Final remaining cash (including sold stocks): {remaining_cash}")

