import yfinance as yf
import pandas as pd

# List of tickers
world_1000_tickers = ['CVCO', 'NMRK', 'NVEI', 'OPTN', 'NVCR', 'ZPTA', 'FNKO', 'NVCT', 'FNLC', 'NVEC', 'TWST', 'BSBK',
                      'UONEK', 'STRT', 'CEAD', 'NMRA', 'SLAB', 'BCG', 'AXON', 'OPTX', 'AGNC', 'SCOR', 'STRR',
                      'IFRX', 'STRS', 'KLXE', 'SCNX', 'SCNI', 'CMRX', 'SDA']

# Function to fetch historical data
def get_historical_data(ticker):
    try:
        stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Function to calculate drop and rebound statistics
def calculate_drop_rebound_stats(stock_data):
    # Calculate daily percentage change
    stock_data['Pct_Change'] = stock_data['Close'].pct_change() * 100

    # Initialize counters
    drop_stats = {f'Drop_{i}%': 0 for i in range(1, 101)}
    rebound_stats = {f'Rebound_{i}%': 0 for i in range(1, 101)}

    # Iterate over the percentage changes
    for i in range(1, len(stock_data)):
        change = stock_data['Pct_Change'].iloc[i]

        # Check for drops
        if change < 0:
            for j in range(1, 101):
                if change <= -j:
                    drop_stats[f'Drop_{j}%'] += 1

        # Check for rebounds
        elif change > 0:
            for j in range(1, 101):
                if change >= j:
                    rebound_stats[f'Rebound_{j}%'] += 1

    return drop_stats, rebound_stats

# Main analysis function
def analyze_tickers(tickers):
    all_drop_stats = {}
    all_rebound_stats = {}

    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        stock_data = get_historical_data(ticker)
        if stock_data is None or stock_data.empty:
            print(f"No data for {ticker}. Skipping.")
            continue

        drop_stats, rebound_stats = calculate_drop_rebound_stats(stock_data)
        all_drop_stats[ticker] = drop_stats
        all_rebound_stats[ticker] = rebound_stats

    return all_drop_stats, all_rebound_stats

# Execute analysis and save results
def main():
    drop_stats, rebound_stats = analyze_tickers(world_1000_tickers)

    # Convert results to DataFrames
    df_drop_stats = pd.DataFrame(drop_stats).T
    df_rebound_stats = pd.DataFrame(rebound_stats).T

    # Save to CSV files
    df_drop_stats.to_csv('drop_statistics.csv')
    df_rebound_stats.to_csv('rebound_statistics.csv')

    print("Analysis complete. Results saved to 'drop_statistics.csv' and 'rebound_statistics.csv'.")

if __name__ == "__main__":
    main()
