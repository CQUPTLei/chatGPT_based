# -*- coding: UTF-8 -*-

from PIL import Image
import base64


# 嵌入信息到图片中
def embed_info(image_path, message, output_path):
    # 把中文转换为base64编码
    message = base64.b64encode(message.encode('utf-8')).decode('ascii')
    # 把信息转换为二进制位
    bits = ''.join(format(ord(x), '08b') for x in message)
    info_len = len(bits)
    # 打开图片
    img = Image.open(image_path)
    # 获取图片的宽度和高度
    width, height = img.size
    # 获取图片的像素数据
    pixels = img.load()
    # 初始化索引
    index = 0
    # 遍历每个像素
    for x in range(width):
        for y in range(height):
            # 获取当前像素的RGB值
            r, g, b = pixels[x, y]
            # 如果还有未嵌入的信息位
            if index < info_len:
                # 把当前像素的红色分量的最低有效位替换为信息位
                r = int(format(r, '08b')[:-1] + bits[index], 2)
                # 索引加一
                index += 1
            # 如果还有未嵌入的信息位
            if index < info_len:
                # 把当前像素的绿色分量的最低有效位替换为信息位
                g = int(format(g, '08b')[:-1] + bits[index], 2)
                # 索引加一
                index += 1
            # 如果还有未嵌入的信息位
            if index < info_len:
                # 把当前像素的蓝色分量的最低有效位替换为信息位
                b = int(format(b, '08b')[:-1] + bits[index], 2)
                # 索引加一
                index += 1
            # 更新当前像素的RGB值
            pixels[x, y] = (r, g, b)
            # 如果已经嵌入了所有的信息位，就退出循环
            if index == len(bits):
                break
        else:
            continue
        break
    # 保存图片到输出路径
    img.save(output_path)
    return info_len


# 从图片中提取信息
def extract_info(image_path, info_len):
    # 打开图片
    img = Image.open(image_path)
    # 获取图片的宽度和高度
    width, height = img.size
    # 获取图片的像素数据
    pixels = img.load()
    # 初始化二进制字符串
    bits = ''
    # 遍历每个像素
    for x in range(width):
        for y in range(height):
            # 获取当前像素的RGB值
            r, g, b = pixels[x, y]
            # 把当前像素的红色分量的最低有效位添加到二进制字符串中
            bits += format(r, '08b')[-1]
            # 把当前像素的绿色分量的最低有效位添加到二进制字符串中
            bits += format(g, '08b')[-1]
            # 把当前像素的蓝色分量的最低有效位添加到二进制字符串中
            bits += format(b, '08b')[-1]
    # 把二进制字符串转换为ASCII码列表
    bits = bits[:info_len]
    chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
    # print(chars)
    # 把ASCII码列表转换为字符串，并去掉末尾可能存在的空字符（\x00）
    message = ''.join(chars).rstrip('\x00')
    # 把base64编码还原为中文
    message = base64.b64decode(message.encode('ascii')).decode('utf-8')
    return message


if __name__ == '__main__':
    # 嵌入信息
    # msg_len = embed_info("B.jpg", "深圳", "SB.jpg")
    # # 提取信息
    # msg = extract_info("SB.jpg", msg_len)
    # print(msg)

    with open('rule1.txt', 'r', encoding='utf-8') as file:
        msg = file.read()
    msg_len = embed_info("NEW.jpg", msg, "SPP.PNG")
    print(msg_len)
    # msg = extract_info("SPP.PNG", msg_len)
    # print(msg)
