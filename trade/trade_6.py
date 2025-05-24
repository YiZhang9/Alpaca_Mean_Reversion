import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fortune 1000 企业列表（假设一些常见的公司）
world_1000_tickers = ['CVCO', 'NMRK', 'NVEI', 'OPTN', 'NVCR', 'ZPTA', 'FNKO', 'NVCT', 'FNLC', 'NVEC', 'TWST', 'BSBK', 'UONEK', 'STRT', 'CEAD', 'NMRA', 'SLAB', 'BCG', 'AXON', 'OPTX', 'AGNC', 'SCOR', 'STRR', 'IFRX', 'STRS', 'KLXE', 'SCNX', 'SCNI', 'CMRX', 'SDA']

# 初始资金分为10份
initial_cash = 10000  # 假设初始资金为10万美元
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}  # 初始持仓为空

# 获取历史数据
def get_historical_data(ticker, moving_average_days):
    stock_data = yf.download(ticker, start="2013-01-01", end="2023-01-01", interval='1d')
    stock_data[f'{moving_average_days}_MA'] = stock_data['Close'].rolling(window=moving_average_days).mean()  # 动态设置均线
    return stock_data

# 回测交易策略
# def backtest_strategy(moving_average_days):
#     cash = initial_cash
#     for ticker in world_1000_tickers:
#         stock_data = get_historical_data(ticker, moving_average_days)
#         for index, row in stock_data.iterrows():
#             current_price = row['Close']
#             moving_avg = row[f'{moving_average_days}_MA']

#             if current_price < moving_avg * 0.94:  # 没有持仓时买入
#                 shares_to_buy = allocation_per_stock // current_price
#                 if shares_to_buy > 0:
#                     portfolio[ticker] += shares_to_buy
#                     cash -= shares_to_buy * current_price

#             elif current_price > moving_avg * 0.96 and portfolio[ticker] > 0:  # 持仓时卖出
#                 shares_to_sell = portfolio[ticker]
#                 portfolio[ticker] = 0
#                 cash += shares_to_sell * current_price
    
#     return cash

def backtest_strategy(moving_average_days):
    cash = initial_cash
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days)
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg = row[f'{moving_average_days}_MA']
                   # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")
                 # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")

            if current_price < moving_avg * 0.79:  # 没有持仓时买入
                shares_to_buy = allocation_per_stock // current_price
                if shares_to_buy > 0:
                    portfolio[ticker] += shares_to_buy
                    cash -= shares_to_buy * current_price
                    # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price} on {index}")


            # 条件2: 如果价格涨回到20日均线的95%，卖出
            elif current_price > moving_avg * 0.96 and portfolio[ticker] > 0:  # 持仓时卖出
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                # print(f"Sold {shares_to_sell} shares of {ticker} at {current_price} on {index}")
    
    # print(f"Final portfolio: {portfolio}")
    # print(f"Remaining cash: {cash}")
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
    for days in range(1319, 1321):  # 测试从100天到109天的均线
        print(f"Testing with {days}-day moving average...")
        cash = backtest_strategy(days)
        remaining_cash = sell_all_positions(cash, days)
        results.append((days, remaining_cash))
        print(f"Final remaining cash with {days}-day MA: {remaining_cash}")
    
    # 打印最终结果
    print("\nResults for different moving average days:")
    for result in results:
        print(f"{result[0]}-day MA: {result[1]} remaining cash")
    df_results = pd.DataFrame(results, columns=['Moving Average Days', 'Remaining Cash'])
    
    # 将结果写入 CSV 文件
    df_results.to_csv('moving_average_test_results_6.csv', index=False)
    print("\nResults saved to 'moving_average_test_results.csv'.")

    plt.figure(figsize=(10, 6))
    plt.plot(df_results['Moving Average Days'], df_results['Remaining Cash'], marker='o', linestyle='-', color='b')
    plt.title('Remaining Cash vs. Moving Average Days')
    plt.xlabel('Moving Average Days')
    plt.ylabel('Remaining Cash')
    plt.grid(True)
    
    # 保存图形
    plt.savefig('moving_average_test_results_plot.png')
    print("\nPlot saved as 'moving_average_test_results_plot.png'.")
    
    # 显示图形
    plt.show()

# 运行测试
test_different_moving_averages()
