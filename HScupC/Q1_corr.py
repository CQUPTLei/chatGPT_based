import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def correlation_analysis(df, num_rows):
    # Select the first num_rows rows
    df_subset = df.iloc[:num_rows]

    # Compute the correlation matrix
    corr = df_subset.corr()

    # Plot the heatmap
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='Greens', cbar=True)
    plt.title('Correlation Heatmap')
    plt.show()


# Call the function
data = pd.read_excel('processed_data.xlsx')
# data = data[data['婴儿行为特征'] == 1.0]
data = data.iloc[:, list(range(1, 10)) + list(range(12, 15))]
correlation_analysis(data, 390)
