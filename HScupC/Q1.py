import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

# # Load the data
# data = pd.read_excel("data.xlsx")
# # Filter the first 390 rows
# data = data[:390]
# # Convert "整晚睡眠时间（时：分：秒）" to hours
# data['整晚睡眠时间（小时）'] = data['整晚睡眠时间（时：分：秒）'].apply(lambda x: x.hour + x.minute / 60 + x.second / 3600)


# # Descriptive statistics
# desc_stats = data.describe(include='all')
# # desc_stats.to_excel('desc_static.xlsx')
# # print(desc_stats)

info = pd.read_excel('processed_data.xlsx')
info = info[:390]

# info = info.iloc[:,8:10]
print(info.head(5))


def Show_body_index(data):
    # Set up the matplotlib figure
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False
    f, axes = plt.subplots(2, 3, figsize=(8, 4))

    # Plot a simple histogram with binsize determined automatically
    sns.histplot(data=data, x="母亲年龄", color="b", kde=True, ax=axes[0, 0])
    # axes[0, 0].set_title('Distribution of Mother\'s Age')
    axes[0, 0].grid(True, alpha=0.3)

    # Plot a kernel density estimate and rug plot
    sns.histplot(data=data, x="婚姻状况", color="r", kde=True, ax=axes[0, 1])
    # axes[0, 1].set_title('Distribution of Mother\'s Age')
    axes[0, 1].grid(True, alpha=0.3)

    # Plot a filled kernel density estimate
    sns.histplot(data=data, x="教育程度", color="g", kde=True, ax=axes[0, 2])
    # axes[0, 2].set_title('Distribution of EPDS Score')
    axes[0, 2].grid(True, alpha=0.3)

    # Plot a histogram and kernel density estimate
    sns.histplot(data=data, x="妊娠时间（周数）", color="m", kde=True, ax=axes[1, 0])
    # axes[1, 0].set_title('Distribution of Baby Age')
    axes[1, 0].grid(True, alpha=0.3)

    # Plot a histogram and kernel density estimate
    sns.histplot(data=data, x="分娩方式", color="m", kde=True, ax=axes[1, 1])
    # axes[1, 1].set_title('Distribution of Baby Age')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def Show_mental_index(data):
    # Set up the matplotlib figure
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
    plt.rcParams['axes.unicode_minus'] = False
    f, axes = plt.subplots(1, 3, figsize=(8, 4))

    # Plot a simple histogram with binsize determined automatically
    sns.histplot(data=data, x='CBTS', color="b", kde=True, ax=axes[0])
    # axes[0, 0].set_title('Distribution of Mother\'s Age')
    axes[0].grid(True, alpha=0.3)

    # Plot a kernel density estimate and rug plot
    sns.histplot(data=data, x="EPDS", color="r", kde=True, ax=axes[1])
    # axes[0, 1].set_title('Distribution of Mother\'s Age')
    axes[1].grid(True, alpha=0.3)

    # Plot a filled kernel density estimate
    sns.histplot(data=data, x="HADS", color="g", kde=True, ax=axes[2])
    # axes[0, 2].set_title('Distribution of EPDS Score')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# Show
# Show_body_index(info[info['婴儿行为特征'] == 1.0])
# Show_body_index(info[info['婴儿行为特征'] == 2.0])
# Show_body_index(info[info['婴儿行为特征'] == 3.0])


Show_mental_index(info[info['婴儿行为特征'] == 1.0])
Show_mental_index(info[info['婴儿行为特征'] == 2.0])
Show_mental_index(info[info['婴儿行为特征'] == 3.0])
