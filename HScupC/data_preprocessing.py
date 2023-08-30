import pandas as pd

# Load the data
df = pd.read_excel("data.xlsx")

# Replace the values in '婴儿行为特征' column with the corresponding numbers
df['婴儿行为特征'].replace({'中等型': 2, '安静型': 1, '矛盾型': 3}, inplace=True)

# Convert '整晚睡眠时间（时：分：秒）' column to hours
df['整晚睡眠时间（小时）'] = df['整晚睡眠时间（时：分：秒）'].apply(lambda x: x.hour + x.minute/60 + x.second/3600 if pd.notnull(x) else x)

# Drop the original '整晚睡眠时间（时：分：秒）' column
df.drop(['整晚睡眠时间（时：分：秒）'], axis=1, inplace=True)

# Save the modified dataframe to a new Excel file
df.to_excel("processed_data.xlsx", index=False)
