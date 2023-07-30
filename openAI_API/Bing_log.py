# -*- coding = utf-8 -*-
# @TIME :     2023-2-28 下午 7:40
# @Author :   CQUPTLei
# @File :     Bing_log.py
# @Software : PyCharm
# @Abstract : Bing写的登录界面

# 导入Tkinter和ttk模块
from tkinter import *
from tkinter import ttk
# 导入hashlib模块
import hashlib

# 定义一个函数，验证用户名和密码是否正确
def login():
    # 获取用户输入的用户名和密码
    username = entry1.get()
    password = entry2.get()
    # 对密码进行加密，并转换为16进制字符串
    password = hashlib.md5(password.encode()).hexdigest()
    # 如果用户名和密码都是admin，则显示登录成功
    if username == "admin" and password == "21232f297a57a5a743894a0e4a801fc3":
        label3.config(text="登录成功")
    # 否则显示登录失败
    else:
        label3.config(text="登录失败")

# 创建一个窗口对象
window = Tk()
# 设置窗口标题
window.title("登录界面")
# 设置窗口大小和位置
window.geometry("300x200+500+300")

# 创建一个标签对象，显示"用户名"
label1 = ttk.Label(window, text="用户名")
# 将标签放置在网格布局中的第一行第一列
label1.grid(row=0, column=0)

# 创建一个输入框对象，接收用户输入的用户名
entry1 = ttk.Entry(window)
# 将输入框放置在网格布局中的第一行第二列
entry1.grid(row=0, column=1)

# 创建一个标签对象，显示"密码"
label2 = ttk.Label(window, text="密码")
# 将标签放置在网格布局中的第二行第一列
label2.grid(row=1, column=0)

# 创建一个输入框对象，接收用户输入的密码，并设置为不可见字符"*"
entry2 = ttk.Entry(window, show="*")
# 将输入框放置在网格布局中的第二行第二列
entry2.grid(row=1, column=1)

# 创建一个按钮对象，点击后调用login函数进行验证
button = ttk.Button(window, text="登录", command=login)
# 将按钮放置在网格布局中的第三行第一列到第三行第二列，并合并单元格
button.grid(row=2, columnspan=2)

# 创建一个标签对象，显示验证结果，默认为空字符串""
label3 = ttk.Label(window, text="")
# 将标签放置在网格布局中的第四行第一列到第四行第二列，并合并单元格
label3.grid(row=3, columnspan=2)

# 进入主循环，等待用户事件发生并处理之
window.mainloop()

