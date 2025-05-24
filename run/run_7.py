import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import os

# Alpaca API 密钥和 Secret
API_KEY = os.getenv('PAPER_API_KEY')  # Use environment variables for security
API_SECRET = os.getenv('PAPER_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets/v2'  # 用于纸面交易（模拟账户）

# 创建 Alpaca API 实例
api = tradeapi.REST(API_KEY, API_SECRET, BASE_URL, api_version='v2')

# 创建 Alpaca Historical Data Client
client = StockHistoricalDataClient(API_KEY, API_SECRET)

# 股票池
world_1000_tickers = world_1000_tickers = [
    'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', \
    'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', \
    'GOOG', 'MO', 'AMZN', 'AMCR', 'AMTM', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', \
    'AWK', 'AMP', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', \
    'AMAT', 'APTV', 'ACGL', 'ADM', 'ANET', 'AJG', 'AIZ', 'T', 'ATO', 'ADSK', \
    'ADP', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC', 'BAX', 'BDX', \
    'BRK.B', 'BBY', 'TECH', 'BIIB', 'BLK', 'BX', 'BK', 'BA', 'BKNG', 'BWA', \
    'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BLDR', 'BG', 'BXP', 'CHRW', \
    'CDNS', 'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CAT', \
    'CBOE', 'CBRE', 'CDW', 'CE', 'COR', 'CNC', 'CNP', 'CF', 'CRL', 'SCHW', \
    'CHTR', 'CVX', 'CMG', 'CB', 'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', \
    'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH', 'CL', 'CMCSA', 'CAG', 'COP', \
    'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CPAY', 'CTVA', 'CSGP', 'COST', \
    'CTRA', 'CRWD', 'CCI', 'CSX', 'CMI', 'CVS', 'DHR', 'DRI', 'DVA', 'DAY', \
    'DECK', 'DE', 'DELL', 'DAL', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DG', \
    'DLTR', 'D', 'DPZ', 'DOV', 'DOW', 'DHI', 'DTE', 'DUK', 'DD', 'EMN', \
    'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA', 'ELV', 'EMR', 'ENPH', 'ETR', \
    'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ERIE', 'ESS', 'EL', 'EG', \
    'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS', 'FICO', \
    'FAST', 'FRT', 'FDX', 'FIS', 'FITB', 'FSLR', 'FE', 'FI', 'FMC', 'F', \
    'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GE', 'GEHC', \
    'GEV', 'GEN', 'GNRC', 'GD', 'GIS', 'GM', 'GPC', 'GILD', 'GPN', 'GL', \
    'GDDY', 'GS', 'HAL', 'HIG', 'HAS', 'HCA', 'DOC', 'HSIC', 'HSY', 'HES', \
    'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ', 'HUBB', \
    'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'INCY', 'IR', 'PODD', \
    'INTC', 'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', \
    'IRM', 'JBHT', 'JBL', 'JKHY', 'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', \
    'KVUE', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KKR', 'KLAC', 'KHC', \
    'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LII', 'LLY', \
    'LIN', 'LYV', 'LKQ', 'LMT', 'L', 'LOW', 'LULU', 'LYB', 'MTB', 'MPC', \
    'MKTX', 'MAR', 'MMC', 'MLM', 'MAS', 'MA', 'MTCH', 'MKC', 'MCD', 'MCK', \
    'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU', 'MSFT', 'MAA', \
    'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS', \
    'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', \
    'NI', 'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', \
    'NXPI', 'ORLY', 'OXY', 'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OTIS', 'PCAR', \
    'PKG', 'PLTR', 'PANW', 'PARA', 'PH', 'PAYX', 'PAYC', 'PYPL', 'PNR', 'PEP', \
    'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PNC', 'POOL', 'PPG', 'PPL', 'PFG', \
    'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM', 'QRVO', 'PWR', \
    'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG', \
    'RMD', 'RVTY', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', \
    'SLB', 'STX', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SW', 'SNA', \
    'SOLV', 'SO', 'LUV', 'SWK', 'SBUX', 'STT', 'STLD', 'STE', 'SYK', 'SMCI', \
    'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR', 'TRGP', 'TGT', 'TEL', \
    'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TPL', 'TXT', 'TMO', 'TJX', 'TSCO', \
    'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UBER', 'UDR', \
    'ULTA', 'UNP', 'UAL', 'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VLTO', \
    'VRSN', 'VRSK', 'VZ', 'VRTX', 'VTRS', 'VICI', 'V', 'VST', 'VMC', 'WRB', \
    'GWW', 'WAB', 'WBA', 'WMT', 'DIS', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', \
    'WELL', 'WST', 'WDC', 'WY', 'WMB', 'WTW', 'WYNN', 'XEL', 'XYL', 'YUM', \
    'ZBRA', 'ZBH', 'ZTS'
]
initial_cash = 100000  
allocation_per_stock = initial_cash / len(world_1000_tickers)
portfolio = {ticker: 0 for ticker in world_1000_tickers}  
cash_history = []  # 用来记录现金余额的变化

def get_historical_data(ticker, moving_average_days):
    print(f"\nFetching historical data for {ticker} with {moving_average_days}-day moving average...")
    
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=TimeFrame.Day,
        start='2000-01-01',  # Modify as per your requirement
        end='2023-12-31'
    )
    
    bars = client.get_stock_bars(request_params)
    
    if bars.df.empty:
        raise ValueError(f"No data found for {ticker}")
    
    stock_df = bars.df[['close']]  # Extract only 'close' column
    print(f"\nFirst 5 rows of fetched data for {ticker}:")
    print(stock_df.head())  # Print first 5 rows of data
    
    input("\nPress Enter to continue...")  # Pause for inspection
    
    # Calculate the moving average
    stock_df[f'{moving_average_days}_MA'] = stock_df['close'].rolling(window=moving_average_days).mean()
    print(f"\nFirst 5 rows with {moving_average_days}-day moving average for {ticker}:")
    print(stock_df.head())  # Print first 5 rows with moving average
    
    input("\nPress Enter to continue...")  # Pause for inspection
    
    return stock_df

def buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash):
    price_ratio = current_price / moving_avg
    print(f"\nChecking buy condition for {ticker} - Current price: {current_price}, Moving Average: {moving_avg}, Price Ratio: {price_ratio}")
    
    if price_ratio <= 0.99:
        if price_ratio >= 0.85:
            buy_percentage = (1 - price_ratio) / (1 - 0.85)
        else:
            buy_percentage = 1

        amount_to_invest = allocation_per_stock * buy_percentage
        shares_to_buy = amount_to_invest // current_price  
        print(f"\nAmount to invest: {amount_to_invest}, Shares to buy: {shares_to_buy}")
        
        if shares_to_buy > 0:
            portfolio[ticker] += shares_to_buy
            cash -= shares_to_buy * current_price
            cash_history.append(cash)  # 记录买入后的现金余额
            
            print(f"\nBuying {shares_to_buy} shares of {ticker}. Cash after buying: {cash}")
            input("\nPress Enter to continue...")  # Pause for inspection
            
            # 使用 Alpaca API 进行买入操作
            api.submit_order(
                symbol=ticker,
                qty=shares_to_buy,
                side='buy',
                type='market',
                time_in_force='gtc'  # Good 'til cancelled
            )
    
    return cash

def backtest_strategy(moving_average_days):
    cash = initial_cash
    cash_history.append(cash)  # 记录初始现金
    print(f"\nStarting backtest for {moving_average_days}-day moving average.")
    
    for ticker in world_1000_tickers:
        stock_data = get_historical_data(ticker, moving_average_days)
        
        for index, row in stock_data.iterrows():
            current_price = row['close']
            moving_avg = row[f'{moving_average_days}_MA']
            print(f"\nProcessing day {index} for {ticker}: Current price: {current_price}, Moving Average: {moving_avg}")
            
            if pd.notna(moving_avg):  
                cash = buy_stock_if_below_threshold(ticker, current_price, moving_avg, cash)

            if current_price > moving_avg and portfolio[ticker] > 0:
                shares_to_sell = portfolio[ticker]
                portfolio[ticker] = 0
                cash += shares_to_sell * current_price
                cash_history.append(cash)  # 记录卖出后的现金余额
                
                print(f"\nSelling {shares_to_sell} shares of {ticker}. Cash after selling: {cash}")
                input("\nPress Enter to continue...")  # Pause for inspection
                
                # 使用 Alpaca API 进行卖出操作
                api.submit_order(
                    symbol=ticker,
                    qty=shares_to_sell,
                    side='sell',
                    type='market',
                    time_in_force='gtc'
                )
    
    return cash

def sell_all_positions(cash, moving_average_days):
    for ticker, shares in portfolio.items():
        if shares > 0:  
            current_price = get_historical_data(ticker, moving_average_days)['close'].iloc[-1]  
            cash += shares * current_price  
            portfolio[ticker] = 0  
            cash_history.append(cash)  # 记录卖出后的现金余额

            print(f"\nSelling all remaining shares of {ticker}. Final cash balance: {cash}")
            input("\nPress Enter to continue...")  # Pause for inspection
            
            # 卖出所有持仓
            api.submit_order(
                symbol=ticker,
                qty=shares,
                side='sell',
                type='market',
                time_in_force='gtc'
            )
    return cash

def test_different_moving_averages():
    results = []
    for days in range(5, 15):  
        print(f"\nTesting with {days}-day moving average...")
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
    df_results.to_csv('moving_average_test_results_run_1.csv', index=False)
    print("\nResults saved to 'moving_average_test_results_run_1.csv'.")

test_different_moving_averages()
