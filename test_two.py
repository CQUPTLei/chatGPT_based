# -*- coding = utf-8 -*-
# @TIME :     2023-1-3 上午 3:08
# @Author :   CQUPTLei
# @File :     test_two.py
# @Software : PyCharm

height = 100.0
distance = 0.0
bounces = 0
while bounces < 10:
    distance += height
    height /= 2.0
    bounces += 1
print("The height of the tenth bounce is", height)
print("The total distance traveled is", distance)
