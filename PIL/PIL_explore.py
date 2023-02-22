# -*- coding = utf-8 -*-
# @TIME :     2023-1-20 下午 1:26
# @Author :   CQUPTLei
# @File :     PIL_explore.py
# @Software : PyCharm
# @Abstract :

import PIL
import os
import matplotlib

os.system('pydoc PIL>PIL_help.md')

from  PIL import  Image

IMG = Image.open('img/cat.png')
IMG.show()