import cv2
import numpy as np
from scipy.fftpack import dct, idct
from reedsolo import RSCodec
import matplotlib.pyplot as plt


def embed_watermark(image_path, watermark_string, block_size=8):
    # 读取图像并转换为YUV颜色空间
    image = cv2.imread(image_path)
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y_channel, u_channel, v_channel = cv2.split(yuv_image)

    # 对Y通道进行DCT变换
    height, width = y_channel.shape
    dct_y_channel = np.zeros_like(y_channel, dtype=float)
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            dct_y_channel[i:(i + block_size), j:(j + block_size)] = cv2.dct(
                np.float32(y_channel[i:(i + block_size), j:(j + block_size)]))

    # 将水印字符串转换为二进制
    watermark_binary = ''.join(format(ord(i), '08b') for i in watermark_string)
    print(watermark_binary)

    # 嵌入水印
    watermark_index = 0
    for i in range(0, height - block_size, block_size):
        for j in range(0, width - block_size, block_size):
            if watermark_index < len(watermark_binary):
                # 修改DCT系数以嵌入水印
                if int(watermark_binary[watermark_index]) == 1:
                    if dct_y_channel[i, j] < 0:
                        dct_y_channel[i, j] = -block_size
                    else:
                        dct_y_channel[i, j] = block_size
                watermark_index += 1

    # 对修改后的Y通道进行逆DCT变换
    idct_y_channel = np.zeros_like(y_channel, dtype=float)
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            idct_y_channel[i:(i + block_size), j:(j + block_size)] = cv2.idct(
                dct_y_channel[i:(i + block_size), j:(j + block_size)])

    # 将修改后的Y通道与U、V通道合并，并转换回BGR颜色空间
    watermarked_image = cv2.cvtColor(cv2.merge([np.uint8(idct_y_channel), u_channel, v_channel]), cv2.COLOR_YUV2BGR)

    return watermarked_image


def extract_watermark(image_path, watermark_length, block_size=8):
    # 读取图像并转换为YUV颜色空间
    image = cv2.imread(image_path)
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y_channel, u_channel, v_channel = cv2.split(yuv_image)

    # 对Y通道进行DCT变换
    height, width = y_channel.shape
    dct_y_channel = np.zeros_like(y_channel, dtype=float)
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            dct_y_channel[i:(i + block_size), j:(j + block_size)] = cv2.dct(
                np.float32(y_channel[i:(i + block_size), j:(j + block_size)]))

    # 提取水印
    watermark_binary = ''
    for i in range(0, height - block_size, block_size):
        for j in range(0, width - block_size, block_size):
            if len(watermark_binary) < watermark_length * 8:
                # 从DCT系数中提取水印
                if dct_y_channel[i, j] > 0:
                    watermark_binary += '1'
                else:
                    watermark_binary += '0'
    print(watermark_binary)
    # 将二进制水印转换为字符串
    watermark_string = ''.join(chr(int(watermark_binary[i:(i + 8)], 2)) for i in range(0, len(watermark_binary), 8))

    return watermark_string


if __name__ == '__main__':
    watermark_string = 'hello'
    image_path = 'B.jpg'

    # 嵌入水印
    watermarked_image = embed_watermark(image_path, watermark_string)
    cv2.imwrite('watermarked_image.PNG', watermarked_image)

    # 提取水印
    extracted_watermark = extract_watermark('watermarked_image.PNG', len(watermark_string))
    print('Extracted watermark:', extracted_watermark)
