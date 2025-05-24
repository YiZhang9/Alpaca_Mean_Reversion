import yfinance as yf
import pandas as pd

# 企业列表
world_1000_tickers = ['CVCO', 'NMRK', 'NVEI', 'OPTN', 'NVCR', 'ZPTA', 'FNKO', 'NVCT', 'FNLC', 'NVEC', 'TWST']

# Function to fetch historical data
def get_historical_data(ticker):
    stock_data = yf.download(ticker, start="2000-01-01", end="2023-01-01", interval='1d')
    if stock_data.empty or 'Close' not in stock_data.columns:
        print(f"Not enough data for {ticker}. Skipping.")
        return None
    stock_data['1319_MA'] = stock_data['Close'].rolling(window=1319).mean()
    return stock_data

# Function to count the frequency of price-to-1319_MA percentages
def count_percent_frequency(stock_data):
    percent_frequency = {}
    
    for index, row in stock_data.iterrows():
        current_price = row['Close']
        moving_avg_1319 = row.get('1319_MA', None)  # Safely get the 1319_MA column
        
        # Skip if the moving average is NaN or not computed
        if pd.isna(moving_avg_1319).any():
            continue
        
        # Ensure current_price and moving_avg_1319 are floats
        current_price = float(current_price)
        moving_avg_1319 = float(moving_avg_1319)
        
        # Calculate the percentage as (current_price / moving_avg_1319) * 100
        percentage = round((current_price / moving_avg_1319) * 100)
        
        # Increment the frequency count for the percentage
        percent_frequency[percentage] = percent_frequency.get(percentage, 0) + 1

    return percent_frequency

# Function to analyze multiple tickers
def analyze_ticker_data(tickers):
    all_frequencies = {}
    for ticker in tickers:
        print(f"Analyzing {ticker}...")
        stock_data = get_historical_data(ticker)
        if stock_data is None:
            continue
        percent_frequency = count_percent_frequency(stock_data)
        all_frequencies[ticker] = percent_frequency
    
    return all_frequencies

# Main function to run the analysis and save results
def main():
    ticker_list = world_1000_tickers[:10]  # Limit to 10 tickers for testing
    all_frequencies = analyze_ticker_data(ticker_list)
    
    # Convert to DataFrame
    result_df = pd.DataFrame(all_frequencies).fillna(0).astype(int)
    result_df.to_csv("percent_frequency_analysis.csv")
    print("Saved results to 'percent_frequency_analysis.csv'")

if __name__ == "__main__":
    main()
