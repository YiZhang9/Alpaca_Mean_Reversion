import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Fortune 1000 企业列表（假设一些常见的公司）
# world_1000_tickers = ['CVCO', 'NMRK', 'NVEI', 'OPTN', 'NVCR', 'ZPTA', 'FNKO', 'NVCT', 'FNLC', 'NVEC', 'TWST', 'BSBK', 
#                       'UONEK', 'STRT', 'CEAD', 'NMRA', 'SLAB', 'BCG', 'AXON', 'OPTX', 'AGNC', 'SCOR', 'STRR', 
#                       'IFRX', 'STRS', 'KLXE', 'SCNX', 'SCNI', 'CMRX', 'SDA']
world_1000_tickers = ['CVCO', 'NVCR', 'FNLC', 'NVEC', 'UONEK', 'STRT', 'CEAD', 'SLAB', 'AXON', 'AGNC', 'SCOR', 'STRR', 'STRS', 'SCNX', 'SCNI', 'CMRX']


# 初始资金分为10份
initial_cash = 10000  # 假设初始资金为10万美元
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}  # 初始持仓为空

# 获取历史数据
def get_historical_data(ticker, moving_average_days):
    stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
    stock_data[f'{moving_average_days}_MA'] = stock_data['Close'].rolling(window=moving_average_days).mean()  # 动态设置均线
    return stock_data

# 买入操作：只要股价低于移动均线的95%就买入
def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash):
    # 计算当前价格相对于移动均线的比值
    price_ratio = current_price / moving_avg

    # 如果股价低于94%就买入
    if price_ratio <= 0.94:
        if price_ratio >= 0.75:
            # 当价格在75%-94%之间时，按比例买入
            buy_percentage = (0.95 - price_ratio) / (0.95 - 0.75)  # 计算买入比例，75% -> 1, 94% -> 0
        else:
            # 当价格低于75%时，买入最大金额（全部资金）
            buy_percentage = 1

        # 计算投入的资金量
        amount_to_invest = allocation_per_stock * buy_percentage
        shares_to_buy = amount_to_invest // current_price  # 根据当前价格计算可以买入多少股

        if shares_to_buy > 0:
            portfolio[ticker] += shares_to_buy
            cash -= shares_to_buy * current_price
            # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price}, investment proportion: {buy_percentage * 100:.2f}%")
    
    return cash



# 回测交易策略
def backtest_strategy(moving_average_days):
    cash = initial_cash
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days)
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg = row[f'{moving_average_days}_MA']

            if isinstance(current_price, pd.Series):
                current_price = current_price.iloc[0]
            if isinstance(moving_avg, pd.Series):
                moving_avg = moving_avg.iloc[0]

            if pd.notna(current_price) and pd.notna(moving_avg):
                current_price = float(row['Close'].iloc[0])
                moving_avg = float(row[f'{moving_average_days}_MA'].iloc[0])

            # 买入操作：股价低于95%时买入
            if pd.notna(moving_avg):  # 确保移动均线已计算
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash)

            # 卖出操作：股价涨回95%以上时卖出
            if current_price > moving_avg * 0.95 and portfolio[ticker] > 0:
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                # print(f"Sold {shares_to_sell} shares of {ticker} at {current_price} after reaching 95%")
    
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
    for days in range(1310,1330):  # 测试从200天到299天的均线
        print(f"Testing with {days}-day moving average...")
        cash = backtest_strategy(days)
        remaining_cash = sell_all_positions(cash, days)
        results.append((days, remaining_cash))
        print(f"Final remaining cash with {days}-day MA: {remaining_cash}")
    
    # 打印最终结果
    print("\nResults for different moving average days:")
    for result in results:
        print(f"{result[0]}-day MA: {result[1]} remaining cash")
    
    # 保存为 DataFrame
    df_results = pd.DataFrame(results, columns=['Moving Average Days', 'Remaining Cash'])
    
    # 将结果写入 CSV 文件
    df_results.to_csv('trade_17.csv', index=False)
    print("\ntrade_17.csv'.")
    
test_different_moving_averages()
