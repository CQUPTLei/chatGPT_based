# -*- coding = utf-8 -*-
# @TIME :     2023-1-7 上午 10:08
# @Author :   CQUPTLei
# @File :     draw.py
# @Software : PyCharm
# @Abstract : 动态地绘制图像
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


def draw_curve():
    # 生成数据
    x = np.linspace(-np.pi, np.pi, 100)
    y = np.sin(x)

    # 创建画布
    fig, ax = plt.subplots()

    # 绘制图像
    line, = ax.plot(x, y)
    plt.show(block=False)

    # 动态更新图像
    while True:
        x += np.pi / 10
        y = np.sin(x)
        line.set_data(x, y)
        plt.pause(0.1)


if __name__=='__main__':
    draw_curve()