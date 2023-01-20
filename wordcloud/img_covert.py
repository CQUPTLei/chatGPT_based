# -*- coding = utf-8 -*-
# @TIME :     2023-1-18 下午 5:19
# @Author :   CQUPTLei
# @File :     img_covert.py
# @Software : PyCharm
# @Abstract : 将图片转换为白底，用于词云的背景图片

from PIL import Image
class Img_Convert:
    def __init__(self,img_name):
        self.name = img_name

    def img_convert(self):
        img = Image.open(fr'img/{self.name}')
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        width = img.width
        height = img.height
        img_new = Image.new('RGB',size=(width,height),color=(255,255,255))
        img_new.paste(img,(0,0),mask=img)
        # img_new.show()
        img_new.save(fr'img/converted_img/{self.name}','png')

if __name__ == '__main__':
    # z在这里填入原图名称(本程序的图片放在img/目录下)
    img_obj = Img_Convert('mask_jay_black.jpeg')
    # 新生成的白底图片放在img/converted_img/目录下
    img_obj.img_convert()