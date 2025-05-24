from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import os
api_key = os.getenv('PAPER_API_KEY')
secret_key = os.getenv('PAPER_API_SECRET')

# print(api_key)
# print(secret_key)
# # Initialize the client
client = StockHistoricalDataClient(api_key, secret_key)

# Define the request parameters
request_params = StockBarsRequest(
    symbol_or_symbols='AAPL',  # Example for Apple stock
    timeframe=TimeFrame.Day,  # Corrected TimeFrame usage
    start='2023-01-01',
    end='2023-12-31'
)

# Get stock bars data
bars = client.get_stock_bars(request_params)

# Print the stock bars data
print(bars)
