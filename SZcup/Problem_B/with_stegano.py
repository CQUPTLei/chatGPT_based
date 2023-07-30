# -*- coding: UTF-8 -*-

from stegano import lsb
# from PIL import Image
import base64


## 先将图片转换为PNG格式
# def convert_to_png(image_path, output_path):
#     img = Image.open(image_path)
#     img.save(output_path, 'PNG')
#
# # 使用函数
# convert_to_png("B.jpg", "P.PNG")


# 嵌入信息到图片中
def embed_info(image_path, message, output_path):
    # 把中文转换为base64编码
    message = base64.b64encode(message.encode('utf-8')).decode('ascii')
    secret = lsb.hide(image_path, message)
    secret.save(output_path)


# 从图片中提取信息
def extract_info(image_path):
    secret_message = lsb.reveal(image_path)
    # 把base64编码还原为中文
    secret_message = base64.b64decode(secret_message.encode('ascii')).decode('utf-8')
    return secret_message


# 嵌入信息
embed_info("P.PNG", "深圳杯数学建模挑战赛", "SP.PNG")

# 提取信息
message = extract_info("SP.PNG")
print(message)



