from PIL import Image, ImageDraw, ImageFont


def add_watermark(image_path, watermark_text, output_path):
    # 打开图片
    img = Image.open(image_path).convert("RGBA")
    # 创建一个和图片大小相同的透明图层
    watermark = Image.new("RGBA", img.size, (0,0,0,0))
    # 设置字体和大小
    font = ImageFont.truetype(r"C:\Windows\Fonts\STCAIYUN.TTF", 40)  # 增大字体大小
    # 获取水印的宽度和高度
    text_width, text_height = font.getbbox(watermark_text)[2:4]
    # 设置水印的位置
    width, height = img.size
    x = width - text_width - 160  # 10px 从右边界开始
    y = height - text_height - 350  # 10px 从底部边界开始
    # 在透明图层上画出水印
    draw = ImageDraw.Draw(watermark, "RGBA")
    # 30, 144, 255, 200
    # 106, 90, 205
    draw.text((x, y), watermark_text, font=font, fill=(250, 128, 114, 250))  #
    # 将水印图层和原图合并
    watermarked = Image.alpha_composite(img, watermark)
    # 保存图片
    watermarked.save(output_path, "PNG")


# 使用示例
add_watermark("third.png", "版权所有：感谢地心引力", "watermarked_image.png")
