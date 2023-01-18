# -*- coding = utf-8 -*-
# @TIME :     2023-1-8 下午 2:10
# @Author :   CQUPTLei
# @File :     search_algorithm.py
# @Software : PyCharm
# @Abstract : 广度优先与深度优先搜索算法

import torch

x = torch.tensor([1, 2, 3])
try:
  print(x.item())
except ValueError as e:
  print(e)  # 输出: can't convert a tensor of size 3 to Python scalar

print(x.tolist())  # 输出: [1, 2, 3]
print(x.numpy())