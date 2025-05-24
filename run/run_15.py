import alpaca_trade_api as tradeapi
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timedelta
import os

# Alpaca API credentials
API_KEY = os.getenv('PAPER_API_KEY')  # Use environment variables for security
API_SECRET = os.getenv('PAPER_API_SECRET')
BASE_URL = 'https://paper-api.alpaca.markets'  # For paper trading accounts

# Initialize Alpaca API
client = StockHistoricalDataClient(API_KEY, API_SECRET)

world_1000_tickers = [
    'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ADBE', 'AMD', 'AES', 'AFL', 'A', \
    'APD', 'ABNB', 'AKAM', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', \
    'GOOG', 'MO', 'AMZN', 'AMCR', 'AMTM', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', \
    # Add other tickers here...
]

# Function to fetch historical data and calculate average
def fetch_average_price(ticker, days):
    """Fetch historical data and calculate the average closing price over the past `days`."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)

    try:
        print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
        request_params = StockBarsRequest(
            symbol_or_symbols=ticker,
            timeframe=TimeFrame.Day,
            start=start_date.strftime('%Y-%m-%d'),
            end=end_date.strftime('%Y-%m-%d')
        )
        bars = client.get_stock_bars(request_params)

        if bars.df.empty:
            raise ValueError(f"No data found for {ticker}")

        # Debug print to show the first and last rows of the fetched data
        print(f"Data for {ticker} fetched successfully. Sample data:\n{bars.df.head()}\n{bars.df.tail()}")

        avg_price = bars.df['close'].mean()  # Calculate the average price
        current_price = bars.df['close'].iloc[-1]  # Get the most recent closing price

        # Debug print for calculated values
        print(f"Ticker: {ticker}, Current Price: {current_price}, Average Price: {avg_price}")

        percentage = (current_price / avg_price) * 100  # Calculate percentage
        return current_price, avg_price, percentage

    except ValueError as ve:
        print(f"Value error for {ticker}: {ve}")
    except Exception as e:
        print(f"General error for {ticker}: {e}")
        # Debug print for detailed exception
        import traceback
        traceback.print_exc()

    return None, None, None

# Function to sort results by percentage
def sort_by_percentage(results):
    """Sort the results by percentage from low to high."""
    try:
        sorted_results = sorted(results, key=lambda x: x['Percentage'])
        return sorted_results
    except Exception as e:
        print(f"Error during sorting: {e}")
        return results

# Calculate and save results to CSV
results = []
for ticker in world_1000_tickers:
    print(f"Processing ticker: {ticker}")
    current_price, avg_price, percentage = fetch_average_price(ticker, 1310)
    if current_price and avg_price:
        results.append({
            'Ticker': ticker,
            'Current Price': current_price,
            '1310-Day Average Price': avg_price,
            'Percentage': percentage
        })
    else:
        print(f"Skipping {ticker} due to missing data.")

# Sort the results
print("Sorting results by percentage...")
sorted_results = sort_by_percentage(results)

# Save sorted results to CSV
current_date = datetime.now().strftime('%Y-%m-%d')
filename = f"{current_date}_sp500_percentages_sorted.csv"
df_sorted_results = pd.DataFrame(sorted_results)
df_sorted_results.to_csv(filename, index=False)

# Print the ticker with the lowest percentage
if sorted_results:
    lowest_percentage_ticker = sorted_results[0]
    print(f"The ticker with the lowest percentage is {lowest_percentage_ticker['Ticker']} "
          f"at {lowest_percentage_ticker['Percentage']:.2f}%.")
else:
    print("No valid results to display.")

print(f"Sorted results saved to {filename}")
