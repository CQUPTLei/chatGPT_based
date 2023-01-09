# -*- coding = utf-8 -*-
# @TIME :     2023-1-9 上午 12:24
# @Author :   CQUPTLei
# @File :     Bilibili_bullet_screen.py
# @Software : PyCharm
# @Abstract : 爬取B站视频弹幕并做成词云
"""
截止本代码创作日，可以获取弹幕xml文件的请求方url有：
（url里面的一串数字是视频的cid）
    https://comment.bilibili.com/176244239.xml
    https://api.bilibili.com/x/v1/dm/list.so?oid=413440316
cid的获取：
    在相应的视频播放也，F12检查，network选项下搜索cid即可。
    Headers里面的RequURL里面就包含有cid
    或者Payload下也有，aid，cid，bvid之类的都有
有空了改进一下，直接通过视频URL湖区cid
"""
import time
import jieba
import requests
from lxml import etree
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class Get_Bilibili_danmu(object):
    # 定义对象属性
    def __init__(self, cid):
        self.cid = cid

    # 下载视频弹幕的xml文件
    def dm_xml(self):
        url = 'https://comment.bilibili.com/' + self.cid+ '.xml'
        try:
            response = requests.get(url)
        except Exception as e:
            print('获取xml内容失败,%s' % e)
            return False
        else:
            if response.status_code == 200:
                with open(f'{self.cid}.xml','wb') as f:
                    f.write(response.content)
                    print('成功下载弹幕xml文件')
                    return True
            else:
                return False

    # 将xml文件中的文本提取出来，去掉停用词，分词
    def get_dm_txt(self):
        # 读取停用词，可以根据结果添加停用词
        with open("ChineseStopWords.txt", "r", encoding="utf-8") as fp:
            stopwords = [s.rstrip() for s in fp.readlines()]
        self.dm_xml()
        time.sleep(5)
        html = etree.parse(f'{self.cid}.xml', etree.HTMLParser())
        # xpath解析，获取当前所有的d标签下的所有文本内容
        text = html.xpath('//d//text()')
        # 列表拼接成字符串
        text = ''.join(text)
        text = jieba.lcut(text)
        words = []
        for w in text:
            if w not in stopwords:
                words.append(w)
        # 注意此处有空格
        words = ' '.join(words)
        return words

    # 生成词云
    def wd(self):
        # collocations用于去掉重复词语；scale值越大清晰度越高，但太大加载会变慢
        wd = WordCloud(font_path='simhei.ttf',colormap="spring",width=800,height=400,
                       collocations=False,scale=5).generate(self.get_dm_txt())
        # 保存图片
        wd.to_file(f'{self.cid}.PNG')
        plt.imshow(wd, interpolation='bilinear')
        plt.axis("off")
        plt.show()




if __name__ == '__main__':
    test_dm = Get_Bilibili_danmu('176244239')
    test_dm.wd()
