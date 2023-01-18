# -*- coding = utf-8 -*-
# @TIME :     2023-1-11 下午 3:06
# @Author :   CQUPTLei
# @File :     wordcloud_resolve.py
# @Software : PyCharm
# @Abstract : wordcloud参数解析与示例

import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
# import cv2

class WD(object):
    # 参数为要生成词云的txt文件名称
    def __init__(self, txt_name):
        self.txt = txt_name

    # 读取要生成词云的txt文件,我已经进行了分词、去除停用词等处理
    def Read_txt(self):
        with open(f'{self.txt}.txt', 'r', encoding='UTF-8') as f:
            dm = f.read()
            return dm

    # 词云制作
    def wd_0(self):
        pic = np.array(Image.open("img/converted_img/flower.png"))
        wd_0 = WordCloud(font_path='simhei.ttf',
                         background_color='black',
                         colormap='spring',
                         width=800, height=400,
                         collocations=False,
                         scale=3,
                         # min_font_size=1,
                         mask=pic,
                         contour_width=10.0,
                         contour_color='white',
                         ).generate(self.Read_txt())
        return wd_0

    # 词云展示
    @staticmethod
    def wd_show(wd):
        plt.imshow(wd, interpolation='bilinear')
        plt.axis("off")
        plt.show()


if __name__ == '__main__':
    dm_obj = WD('anhao_dm')
    # 选择一个例子生成词云
    wd = dm_obj.wd_0()
    wd.to_file(f'img/wd_output_img/out.PNG')
    dm_obj.wd_show(wd)
