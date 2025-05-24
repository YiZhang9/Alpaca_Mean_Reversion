import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca_trade_api.rest import REST

# Alpaca API 密钥和 Secret (需要替换成你的实际密钥)
API_KEY = 'PKLXDAMFPFY0F3RM9GX0'
API_SECRET = 'XGGeEaRvTx5SSyAvRdEFaGPfMi6yrYiJfxbHLStc'
BASE_URL = 'https://paper-api.alpaca.markets'  # 实际账户的URL

# 创建 Alpaca API 实例
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# 股票池
world_1000_tickers = ['AAPL', 'TSLA']

initial_cash = 100000  
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}  
cash_history = []  # 用来记录现金余额的变化

# 获取历史数据
def get_historical_data(ticker, moving_average_days):
    try:
        # 请求较短的历史数据，50天内
        barset = api.get_bars(ticker, tradeapi.rest.TimeFrame.Day, limit=50)
        
        if not barset:
            print(f"No data returned for {ticker}")
            return None
        
        # 正常处理数据
        data = {'Close': [bar.c for bar in barset]}
        stock_df = pd.DataFrame(data)
        stock_df[f'{moving_average_days}_MA'] = stock_df['Close'].rolling(window=moving_average_days).mean()
        
        print(stock_df)  # 打印返回的 dataframe
        
        return stock_df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None


# 买入逻辑
def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash):
    price_ratio = current_price / moving_avg
    print(f"Ticker: {ticker}, Current Price: {current_price}, Moving Avg: {moving_avg}, Price Ratio: {price_ratio}")

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

            # 提交买入订单
            api.submit_order(
                symbol=ticker,
                qty=shares_to_buy,
                side='buy',
                type='market',
                time_in_force='gtc'
            )
            print(f"Submitted buy order for {shares_to_buy} shares of {ticker}")
    
    return cash

# 回测策略
def backtest_strategy(moving_average_days):
    cash = initial_cash
    cash_history.append(cash)  # 记录初始现金
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days)
        
        if stock_data is None or stock_data.empty:
            print(f"Skipping {ticker} due to no data")
            continue  # 如果没有数据，跳过当前股票

        for index, row in stock_data.iterrows():
            current_price = row['Close']
            moving_avg = row[f'{moving_average_days}_MA']

            if pd.notna(moving_avg):  
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash)

            # 卖出逻辑
            if current_price > moving_avg * 1 and portfolio[ticker] > 0:
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                cash_history.append(cash)  # 记录卖出后的现金余额

                # 提交卖出订单
                api.submit_order(
                    symbol=ticker,
                    qty=shares_to_sell,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
    
    return cash


# 卖出所有持仓
def sell_all_positions(cash, moving_average_days):
    for ticker, shares in portfolio.items():
        if shares > 0:  
            current_price = get_historical_data(ticker, moving_average_days)['Close'].iloc[-1]  
            cash += shares * current_price  
            portfolio[ticker] = 0  
            cash_history.append(cash)  # 记录卖出后的现金余额

            # 卖出所有持仓
            api.submit_order(
                symbol=ticker,
                qty=shares,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
    return cash

# 获取账户信息
def get_account_info():
    account = api.get_account()
    print(f"Current Account Equity: {account.equity}")
    print(f"Current Profit/Loss: {float(account.equity) - float(account.cash)}")

# 执行实际策略
def execute_strategy():
    moving_average_days = 1321  # 固定为1321天的移动平均线
    cash = initial_cash
    cash_history.append(cash)
    cash = backtest_strategy(moving_average_days)
    remaining_cash = sell_all_positions(cash, moving_average_days)
    get_account_info()  # 获取账户信息并显示当前盈亏情况

execute_strategy()  # 执行策略
