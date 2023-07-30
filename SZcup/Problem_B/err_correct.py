from PIL import Image
from reedsolo import RSCodec


def embed_LSB_with_error_correction(image_path, data, ecc_bytes):
    # 打开图像并转换为可操作的像素数组
    image = Image.open(image_path)
    pixels = image.load()

    # 使用Reed-Solomon编码对数据进行纠错编码
    rs = RSCodec(ecc_bytes)
    encoded_data = rs.encode(data)

    # 将数据转换为二进制格式
    binary_data = ''.join(format(i, '08b') for i in encoded_data)

    # 嵌入数据
    data_index = 0
    for row in range(image.height):
        for col in range(image.width):
            r, g, b = pixels[col, row]

            # 修改像素的最低有效位
            if data_index < len(binary_data):
                # 红色通道
                r = (r & 0xFE) | int(binary_data[data_index], 2)
                data_index += 1
            if data_index < len(binary_data):
                # 绿色通道
                g = (g & 0xFE) | int(binary_data[data_index], 2)
                data_index += 1
            if data_index < len(binary_data):
                # 蓝色通道
                b = (b & 0xFE) | int(binary_data[data_index], 2)
                data_index += 1

            # 将修改后的像素写回图像
            pixels[col, row] = (r, g, b)

    return image


def extract_LSB_with_error_correction(image_path, data_length, ecc_bytes):
    # 打开图像并转换为可操作的像素数组
    image = Image.open(image_path)
    pixels = image.load()

    # 提取数据
    binary_data = ''
    for row in range(image.height):
        for col in range(image.width):
            r, g, b = pixels[col, row]

            # 从像素的最低有效位提取数据
            if len(binary_data) < data_length * 8:
                # 红色通道
                binary_data += str(r & 1)
            if len(binary_data) < data_length * 8:
                # 绿色通道
                binary_data += str(g & 1)
            if len(binary_data) < data_length * 8:
                # 蓝色通道
                binary_data += str(b & 1)

    # 将二进制数据转换为字节
    extracted_data = bytearray(int(binary_data[i:i + 8], 2) for i in range(0, len(binary_data), 8))

    # 使用Reed-Solomon编码对数据进行纠错解码
    rs = RSCodec(ecc_bytes)
    decoded_data = rs.decode(extracted_data)

    return decoded_data


if __name__ == '__main__':
    img = embed_LSB_with_error_correction('B.jpg', '深圳杯数学建模挑战赛'.encode('utf-8'), 100)
    img.save('SPP.PNG')

    msg = extract_LSB_with_error_correction('SPP.PNG', len('深圳杯数学建模挑战赛'.encode('utf-8')) + 100, 100)
    print(msg[0].decode('utf-8'))

