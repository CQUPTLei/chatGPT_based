# 数据预处理
import pandas as pd
# Load the data
data = pd.read_excel("data.xlsx")
# Select the first 390 rows
data_390 = data.iloc[:390]
# Convert "整晚睡眠时间（时：分：秒）" column to datetime.time objects
data_390["整晚睡眠时间（时：分：秒）"] = pd.to_datetime(data_390["整晚睡眠时间（时：分：秒）"], format='%H:%M:%S').dt.time
# Filter the dataframe based on the conditions: 睡醒次数 = 0 and 入睡方式 = 4
filtered_data = data_390[(data_390["睡醒次数"] == 0) & (data_390["入睡方式"] == 4)]
# Convert sleep time to total minutes for calculation
filtered_data["整晚睡眠时间（分钟）"] = filtered_data["整晚睡眠时间（时：分：秒）"].apply(lambda x: x.hour * 60 + x.minute)
# Calculate the average sleep time
average_sleep_time = filtered_data["整晚睡眠时间（分钟）"].mean()
# Convert the average sleep time back to the time format
average_sleep_time_hours = int(average_sleep_time // 60)
average_sleep_time_minutes = int(average_sleep_time % 60)
print(f'The average sleep time for records with 睡醒次数 = 0 and 入睡方式 = 4 is {average_sleep_time_hours} hours and {average_sleep_time_minutes} minutes.')
