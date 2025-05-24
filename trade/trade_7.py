import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Fortune 1000 企业列表
world_1000_tickers = ['CVCO', 'NVCR', 'FNLC', 'NVEC', 'UONEK', 'STRT', 'CEAD', 'SLAB', 'AXON', 'AGNC', 'SCOR', 'STRR', 'STRS', 'SCNX', 'SCNI', 'CMRX']

# 初始资金分为10份
initial_cash = 10000  # 假设初始资金为10万美元
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}  # 初始持仓为空

# 获取历史数据
def get_historical_data(ticker, moving_average_days, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    stock_data[f'{moving_average_days}_MA'] = stock_data['Close'].rolling(window=moving_average_days).mean()  # 动态设置均线
    return stock_data

# 买入操作：只要股价低于移动均线的95%就买入
def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash):
    # 计算当前价格相对于移动均线的跌幅百分比
    drop_percent = (moving_avg - current_price) / moving_avg

    # 如果股价低于均线的95%就开始买入
    if current_price < moving_avg * 0.95:
        # 使用一个比例来确定买入的资金分配
        # 当跌至均线的94%时，买入最少；当跌至均线的1%时，买入最大
        # 这里使用线性比例，最多买入allocation_per_stock的全部，最少买入1%
        buy_percentage = min(1, drop_percent / 0.94)  # 最大买入比例为1
        amount_to_invest = allocation_per_stock * buy_percentage  # 计算这次要投入的金额
        shares_to_buy = amount_to_invest // current_price  # 根据当前价格计算可以买入多少股

        if shares_to_buy > 0:
            portfolio[ticker] += shares_to_buy
            cash -= shares_to_buy * current_price
            # print(f"Bought {shares_to_buy} shares of {ticker} at {current_price}, investment proportion: {buy_percentage * 100:.2f}%")
    
    return cash

# 回测交易策略
def backtest_strategy(moving_average_days, start_date, end_date):
    cash = initial_cash
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days, start_date, end_date)
        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg = row[f'{moving_average_days}_MA']

            if pd.notna(moving_avg):  # 确保移动均线已计算
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash)

            # 卖出操作：当价格涨回到95%以上时卖出
            if current_price > moving_avg * 0.95 and portfolio[ticker] > 0:
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                # print(f"Sold {shares_to_sell} shares of {ticker} at {current_price}")
    
    return cash

# 清算所有持仓
def sell_all_positions(cash, moving_average_days, start_date, end_date):
    for ticker, shares in portfolio.items():
        if shares > 0:  # 如果有持仓
            current_price = get_historical_data(ticker, moving_average_days, start_date, end_date)['Close'].iloc[-1]  # 获取最后一天的价格
            cash += shares * current_price  # 将股票市值转化为现金
            portfolio[ticker] = 0  # 清空持仓
    return cash

# 测试不同的均线天数和不同的开始日期
def test_different_moving_averages_and_dates():
    results = []
    # 设置日期范围
    start_test_date = datetime(2000, 1, 1)
    end_test_date = datetime(2023, 1, 1)
    
    # 日期测试范围为2000年1月1日到2022年12月31日
    current_test_date = start_test_date
    delta_one_day = timedelta(days=1)

    while current_test_date <= datetime(2022, 12, 31):
        row_result = []  # 存储每个开始日期的结果
        for days in range(1, 2001):  # 测试1到2000天的均线
            print(f"Testing {days}-day moving average from {current_test_date.strftime('%Y-%m-%d')}")
            cash = backtest_strategy(days, current_test_date.strftime('%Y-%m-%d'), end_test_date.strftime('%Y-%m-%d'))
            remaining_cash = sell_all_positions(cash, days, current_test_date.strftime('%Y-%m-%d'), end_test_date.strftime('%Y-%m-%d'))
            row_result.append(remaining_cash)
            print(f"Remaining cash with {days}-day MA starting from {current_test_date.strftime('%Y-%m-%d')}: {remaining_cash}")
        
        # 将该日期下的结果添加到结果列表
        results.append([current_test_date.strftime('%Y-%m-%d')] + row_result)
        current_test_date += delta_one_day  # 增加一天，进行下一次测试

    # 生成 DataFrame，列名为均线天数，行名为日期
    df_results = pd.DataFrame(results, columns=['Start Date'] + [f'{i}-day MA' for i in range(1, 2001)])
    
    # 将结果写入 CSV 文件
    df_results.to_csv('moving_average_test_results_with_dates.csv', index=False)
    print("\nResults saved to 'moving_average_test_results_with_dates.csv'.")

# 运行测试
test_different_moving_averages_and_dates()
