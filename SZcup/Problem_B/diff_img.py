#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023-7-29 上午 7:43
# @Author  : dahu
# @FileName: diff_img
# @Software: PyCharm
# @Abstract : 摘要

# 导入所需的库
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


# 定义MSE函数
def mse(imageA, imageB):
    # 计算两张图片之间的均方误差
    # 两张图片必须有相同的尺寸
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # 返回MSE值，越小越相似
    return err


# 读取两张图片
imageA = cv2.imread("B.jpg")
imageB = cv2.imread("SPP.PNG")

# 将图片转换为灰度图
imageA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
imageB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# 计算两张图片的MSE和SSIM值
m = mse(imageA, imageB)
s = ssim(imageA, imageB)

# 打印结果
print("MSE: %.8f" % m)
print("SSIM: %.8f" % s)
