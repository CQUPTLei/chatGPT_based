import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.fftpack import dct, idct


# 加载原始图像和水印图像
def load_images(original_image_path, watermark_image_path):
    try:
        original_image = Image.open(original_image_path)
        watermark_image = Image.open(watermark_image_path)
    except FileNotFoundError:
        print("无法找到图像文件，请检查文件路径是否正确。")
        exit()
    return original_image, watermark_image


# 调整水印图像的大小以匹配原始图像
def resize_watermark(original_image, watermark_image):
    watermark_size = (original_image.size[0] // 8, original_image.size[1] // 8)
    watermark_image = watermark_image.resize(watermark_size).convert('RGB')
    return watermark_image

# 将图像转换为numpy数组
def image_to_array(image):
    return np.array(image)


# 对原始图像执行离散余弦变换（DCT）
def perform_dct(original_array):
    height, width, _ = original_array.shape
    dct_blocks = np.empty_like(original_array, dtype=np.float64)
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            dct_blocks[i:i + 8, j:j + 8] = dct(dct(original_array[i:i + 8, j:j + 8], axis=0, norm='ortho'), axis=1,
                                               norm='ortho')
    return dct_blocks


# 将水印嵌入到DCT块中
def embed_watermark(dct_blocks, watermark_array, alpha=0.05):
    dct_blocks_with_watermark = dct_blocks.copy()
    dct_blocks_with_watermark[::8, ::8] += alpha * watermark_array
    return dct_blocks_with_watermark


# 对带有水印的DCT块执行逆离散余弦变换（IDCT）
def perform_idct(dct_blocks_with_watermark):
    height, width, _ = dct_blocks_with_watermark.shape
    image_with_watermark = np.empty_like(dct_blocks_with_watermark)
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            image_with_watermark[i:i + 8, j:j + 8] = idct(
                idct(dct_blocks_with_watermark[i:i + 8, j:j + 8], axis=0, norm='ortho'), axis=1, norm='ortho')
    return image_with_watermark


# 将图像的值裁剪到有效范围并转换为uint8
def clip_and_convert(image_with_watermark):
    image_with_watermark = np.clip(image_with_watermark, 0, 255).astype(np.uint8)
    return image_with_watermark


# 将numpy数组转换回图像
def array_to_image(image_array):
    return Image.fromarray(image_array)


# 处理图像的主函数
def process_images(original_image_path, watermark_image_path, alpha=0.05):
    # 加载图像
    original_image, watermark_image = load_images(original_image_path, watermark_image_path)
    # 调整水印大小
    watermark_image = resize_watermark(original_image, watermark_image)
    # 将图像转换为数组
    original_array = image_to_array(original_image)
    watermark_array = image_to_array(watermark_image)
    # 对原始图像执行DCT
    dct_blocks = perform_dct(original_array)
    # 嵌入水印
    dct_blocks_with_watermark = embed_watermark(dct_blocks, watermark_array, alpha)
    # 执行IDCT
    image_with_watermark = perform_idct(dct_blocks_with_watermark)
    # 裁剪和转换图像
    image_with_watermark = clip_and_convert(image_with_watermark)
    # 将数组转换回图像
    image_with_watermark = array_to_image(image_with_watermark)
    return image_with_watermark


# 使用函数
image_with_watermark = process_images('20.png', 'watermark.png', alpha=0.8)
image_with_watermark.save('2020E.PNG')
