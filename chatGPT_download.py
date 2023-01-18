# -*- coding = utf-8 -*-
# @TIME :     2023-1-7 下午 8:32
# @Author :   CQUPTLei
# @File :     chatGPT_download.py
# @Software : PyCharm
# @Abstract :

import requests
from bs4 import BeautifulSoup

# 视频地址
url = "https://www.bilibili.com/video/BV1zE41127Qh"

# 获取视频页面
r = requests.get(url)

# 解析页面
soup = BeautifulSoup(r.text, "html.parser")

# 找到视频地址
video_url = soup.find("source")["src"]

# 下载视频
r = requests.get(video_url)

# 保存视频
with open("video.mp4", "wb") as f:
    f.write(r.content)

