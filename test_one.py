# -*- coding = utf-8 -*-
# @TIME :     2023-1-3 上午 2:42
# @Author :   CQUPTLei
# @File :     test_one.py
# @Software : PyCharm
# @Abstract :动态地绘制曲面

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d


def draw_surface():
    # 生成数据
    x = np.linspace(-np.pi, np.pi, 100)
    y = np.linspace(-np.pi, np.pi, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.sin(Y)

    # 绘制图像
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()
