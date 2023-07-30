# -*- coding = utf-8 -*-
# @TIME :     2023-2-22 下午 9:10
# @Author :   CQUPTLei
# @File :     GPT_gui_1.py
# @Software : PyCharm
# @Abstract : 可连续对话
import inspect
import openai

module = inspect.getmodule(openai.Completion.create)
members = inspect.getmembers(module)

for name, member in members:
    if inspect.ismodule(member):
        print(name)

