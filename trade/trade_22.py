import pandas as pd
from io import StringIO

# Creating the list for the 'Adj Close' column from the provided data, in reverse order
data = [
    181.79, 187.71, 190.63, 192.94, 194.23, 193.55, 193.22, 191.48, 190.80, 187.12,
    183.50, 185.95, 184.94, 186.77, 188.38, 188.49, 187.40, 188.17, 186.48, 184.37,
    183.49, 183.20, 181.65, 180.91, 181.66, 183.71, 181.86, 180.51, 181.97, 180.77,
    180.10, 179.01, 174.47, 169.51, 168.51, 168.39, 170.11, 172.13, 172.61, 170.51,
    172.38, 172.00, 173.09, 175.45, 178.03, 170.75, 171.66, 170.23, 169.10, 172.69,
    170.86, 169.42, 168.23, 169.04, 168.21, 168.97, 167.84, 169.06, 167.18, 174.41,
    175.91, 172.07, 168.77, 167.39, 166.44, 164.41, 165.24, 166.30, 168.41, 169.28,
    168.69, 172.87, 169.72, 168.69, 172.41, 182.72, 181.05, 181.74, 182.08, 183.90,
    182.64, 185.86, 187.01, 189.29, 189.41, 189.44, 190.61, 191.92, 190.47, 186.46,
    189.55, 189.56, 189.86, 190.86, 191.82, 193.59, 193.91, 195.43, 194.04, 194.48,
    196.45, 192.68, 206.68, 212.59, 213.76, 212.01, 216.18, 213.81, 209.21, 207.02,
    207.67, 208.60, 212.77, 213.62, 210.15, 216.26, 219.77, 221.05, 225.83, 227.31,
    228.16, 232.45, 227.06, 230.02, 233.87, 234.29, 228.36, 223.67, 223.80, 223.46,
    224.50, 218.05, 217.00, 217.47, 217.75, 218.31, 221.58, 217.87, 219.36, 208.80,
    206.76, 209.35, 212.83, 215.75, 217.29, 224.47, 225.80, 226.93, 227.78, 226.24,
    224.28, 226.59, 226.93, 227.52, 227.54, 232.74, 225.96, 226.53, 225.42, 228.79,
    227.30, 231.05, 233.59, 231.53, 234.74, 236.22, 235.60, 230.32, 231.16, 233.14,
    233.41, 229.85, 225.66, 222.67, 220.58, 222.53, 222.42, 222.26, 216.08, 216.55,
    220.45, 228.62, 227.95, 226.22, 227.12, 226.12, 227.27, 225.42, 229.54, 228.79,
    227.30, 226.40, 225.83, 223.46, 224.50, 224.28, 228.62, 228.87, 230.51, 235.60,
    236.22, 236.85, 243.36, 245.00, 242.21, 242.70, 236.85, 234.40, 233.28, 237.87,
    228.26
]

# Initialize cash and stock holdings
cash = 100000  # Starting cash in dollars
stocks = 0  # Starting stock quantity

# Loop through the 'data' list to simulate trading
for i in range(1, len(data)):
    if data[i] > data[i - 1]:  # Price went up
        # Sell all stocks
        if stocks > 0:
            cash += stocks * data[i]
            print(f"Day {i}: Price up to {data[i]:.2f}. Sold {stocks} stocks for ${stocks * data[i]:.2f}.")
            stocks = 0
        else:
            print(f"Day {i}: Price up to {data[i]:.2f}. No stocks to sell.")
    elif data[i] < data[i - 1]:  # Price went down
        # Buy as many stocks as possible
        stocks_to_buy = cash // data[i]
        if stocks_to_buy > 0:
            stocks += stocks_to_buy
            cash -= stocks_to_buy * data[i]
            print(f"Day {i}: Price down to {data[i]:.2f}. Bought {stocks_to_buy} stocks for ${stocks_to_buy * data[i]:.2f}.")
        else:
            print(f"Day {i}: Price down to {data[i]:.2f}. Not enough cash to buy stocks.")
    else:
        # Price stayed the same; no action
        print(f"Day {i}: Price unchanged at {data[i]:.2f}. No action taken.")

# Final portfolio value
final_value = cash + stocks * data[-1]
print(f"\nFinal Portfolio Value: ${final_value:.2f}")
print(f"Remaining Cash: ${cash:.2f}")
print(f"Stocks Held: {stocks}")
