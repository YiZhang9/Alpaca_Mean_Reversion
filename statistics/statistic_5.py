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
        if stock_data.empty:
            print(f"Data for {ticker} is empty.")
            return None
        return stock_data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

# Function to calculate current price to 1319-MA percent statistics
def calculate_price_to_moving_avg_stats(stock_data):
    if 'Close' not in stock_data.columns:
        print("No 'Close' column found. Skipping.")
        return {f'{i}%': 0 for i in range(50, 201)}

    # Calculate 1319-day moving average
    stock_data['1319_MA'] = stock_data['Close'].rolling(window=1319).mean()

    # Check if '1319_MA' is calculated
    if stock_data['1319_MA'].isna().all():
        print("Insufficient data to calculate 1319-day moving average.")
        return {f'{i}%': 0 for i in range(50, 201)}

    # Filter rows where the 1319-MA is not NaN
    valid_data = stock_data.dropna(subset=['1319_MA'])

    # Calculate the ratio of Close to 1319-MA in percentages
    valid_data['Price_to_1319MA_Percent'] = (valid_data['Close'] / valid_data['1319_MA']) * 100

    # Initialize counters
    percent_ranges = {f'{i}%': 0 for i in range(50, 201)}  # Percentages from 50% to 200%

    # Iterate over the percentage values and count occurrences in each range
    for percent in valid_data['Price_to_1319MA_Percent']:
        rounded_percent = int(percent)
        if 50 <= rounded_percent <= 200:
            percent_ranges[f'{rounded_percent}%'] += 1

    return percent_ranges

# Main analysis function
def analyze_tickers(tickers):
    all_percent_stats = {}

    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        stock_data = get_historical_data(ticker)
        if stock_data is None:
            print(f"{ticker} skipped due to insufficient data.")
            continue

        percent_stats = calculate_price_to_moving_avg_stats(stock_data)
        all_percent_stats[ticker] = percent_stats

    return all_percent_stats

# Execute analysis and save results
def main():
    percent_stats = analyze_tickers(world_1000_tickers)

    # Convert results to DataFrame
    df_percent_stats = pd.DataFrame(percent_stats).T

    # Save to CSV file
    df_percent_stats.to_csv('price_to_1319MA_statistics.csv')

    print("Analysis complete. Results saved to 'price_to_1319MA_statistics.csv'.")

if __name__ == "__main__":
    main()
