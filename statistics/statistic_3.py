import pandas as pd

# 读取CSV文件
df = pd.read_csv('drop_and_rebound_earn.csv')

# 创建一个新的 DataFrame 用于保存结果
result_df = pd.DataFrame()

# 遍历每一行，计算总和并乘以行号（从1开始）
result_df['Sum_Multiplied'] = [df.iloc[i, 1:].sum() * (i + 1) for i in range(len(df))]

# 将结果保存为一个新的CSV文件
result_df.to_csv('drop_and_rebound_analysis_sum_multiplied.csv', index=False)

# 输出保存成功信息
print("新的表格已经生成并保存为 'drop_and_rebound_analysis_sum_multiplied.csv'")
