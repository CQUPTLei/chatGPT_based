#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023-8-16 上午 10:01
# @Author  : dahu
# @FileName: test
# @Software: PyCharm
# @Abstract : 摘要

import itertools as its
words = "1234567890abcdefghijklmnopqrstuvwxyz" #可选择的字符
r =its.product(words,repeat=8)  #组成8位字符串
dic = open("pwd.txt","a")      #存储为wifi密码字典
#wifi密码完成换行，并写入txt文档
for i in r:
    dic.write("".join(i))
    dic.write("".join("\n"))
dic.close()
