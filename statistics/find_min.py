import pandas as pd

# 读取 cash_history CSV 文件
cash_history_df = pd.read_csv('cash_history_1310_days_MA.csv')

# 找出 'Cash Balance' 列中的最小值
min_cash_balance = cash_history_df['Cash Balance'].min()

# 打印最小值
print(f"The minimum cash balance is: {min_cash_balance}")
