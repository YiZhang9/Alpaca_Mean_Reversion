import pandas as pd

# 读取CSV文件
df = pd.read_csv('drop_and_rebound_analysis.csv')

# 提取第1列的百分比并去掉%符号，计算涨回的百分比（95% - 当前百分比）
df['Gain_Percentage'] = 95 - df.iloc[:, 0].str.rstrip('%').astype(int)

# 将不同公司列的次数乘以涨回的百分比，然后对每个百分比的总收益进行求和
df['Total_Earnings'] = df['Gain_Percentage'] * df.iloc[:, 1:].sum(axis=1)

# 将总收益作为最后一列添加到原始表格
df_with_earnings = df.copy()  # 创建表格副本
df_with_earnings['Total_Earnings'] = df['Total_Earnings']  # 添加总收益列

# 保存为新的CSV文件，或者你也可以选择替换原文件
df_with_earnings.to_csv('drop_and_rebound_analysis_with_earnings.csv', index=False)

# 输出更新后的表格
print("更新后的表格:")
print(df_with_earnings)
