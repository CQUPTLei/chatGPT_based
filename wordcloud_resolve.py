# -*- coding = utf-8 -*-
# @TIME :     2023-1-11 下午 3:06
# @Author :   CQUPTLei
# @File :     wordcloud_resolve.py
# @Software : PyCharm
# @Abstract : wordcloud参数解析与示例
import wordcloud
import time
import jieba
import requests
from lxml import etree
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class WD(object):
    # def __init__(self,dm_txt):
    #     self.dm_txt = dm_txt

    # 读取要生成词云的txt文件,我已经进行了分词、去除停用词等处理
    @staticmethod
    def Read_txt():
        with open('anhao_dm.txt','r',encoding='UTF-8') as f:
            dm = f.read()
            return dm

    # 词云制作
    @staticmethod
    def wd_0(self):
        wd_0 = WordCloud.generate(self,WD.Read_txt())
        return wd_0

    # 词云展示
    def wd_show(self):
        plt.imshow(wd, interpolation='bilinear')
        plt.axis("off")
        plt.show()



if __name__ == '__main__':
    dm_obj = WD()
    dm_obj.wd_show()

