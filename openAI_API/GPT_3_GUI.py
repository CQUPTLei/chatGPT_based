# -*- coding = utf-8 -*-
# @TIME :     2023-2-21 下午 10:55
# @Author :   CQUPTLei
# @File :     GPT_3_GUI.py
# @Software : PyCharm
# @Abstract :

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import requests

# 创建窗口
window = tk.Tk()
window.title('GPT-3')
window.geometry('400x400')

# 创建文本框
e = tk.Entry(window, show=None, font=('Arial', 14))
e.pack()

# 创建按钮
def send():
    # 获取文本框内容
    content = e.get()
    # 调用GPT-3
    response = requests.post('https://api.openai.com/v1/engines/davinci/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer <API_KEY>'
        },
        json={
            'prompt': content,
            'max_tokens': 50
        }
    )
    # 获取GPT-3返回的结果
    result = response.json()['choices'][0]['text']
    # 弹出消息框
    messagebox.showinfo(title='GPT-3', message=result)

b = tk.Button(window, text='Send', font=('Arial', 14), width=10, height=1, command=send)
b.pack()

# 主程序
window.mainloop()root.mainloop()