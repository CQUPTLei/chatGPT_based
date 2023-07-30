# -*- coding = utf-8 -*-
# @TIME :     2023-2-28 下午 7:05
# @Author :   CQUPTLei
# @File :     Bing_token_ring.py
# @Software : PyCharm
# @Abstract :

# 定义一个类来表示主机
class Host:
    def __init__(self, name):
        self.name = name  # 主机名
        self.data = None  # 要发送的数据
        self.token = False  # 是否拥有令牌

    def send(self, data):
        # 如果拥有令牌，就发送数据，并释放令牌
        if self.token:
            print(f"{self.name} 发送了 {data}")
            self.data = None
            self.token = False

    def receive(self, data):
        # 如果没有令牌，就接收数据，并检查是否是自己的数据
        if not self.token:
            print(f"{self.name} 接收了 {data}")
            if data.startswith(self.name):
                print(f"{self.name} 收到了自己的数据")

    def request(self, data):
        # 如果没有数据要发送，就请求发送数据，并存储在自己的缓冲区中
        if not self.data:
            print(f"{self.name} 请求发送 {data}")
            self.data = f"{self.name}->{data}"


# 定义一个函数来模拟网络传输
def transmit(hosts):
    # 找到拥有令牌的主机，并将其索引存储在变量 i 中
    i = 0
    for host in hosts:
        if host.token:
            break
        i += 1

    # 循环遍历主机列表，模拟令牌在环中传递
    while True:
        # 获取当前主机和下一个主机（如果到达列表末尾，就回到列表开头）
        current_host = hosts[i]
        next_host = hosts[(i + 1) % len(hosts)]

        # 如果当前主机有数据要发送，就调用 send 方法，并将数据传给下一个主机
        if current_host.data:
            current_host.send(current_host.data)
            next_host.receive(current_host.data)

        # 如果当前主机没有数据要发送，但下一个主机有请求发送的数据，就将令牌传给下一个主机，并调用 send 方法
        elif next_host.data:
            current_host.token = False
            next_host.token = True
            next_host.send(next_host.data)

        # 否则，什么都不做

        # 更新 i 的值，指向下一个主机的索引（如果到达列表末尾，就回到列表开头）
        i = (i + 1) % len(hosts)


# 创建四个主机对象，并将其中一个赋予初始令牌
hostA = Host("A")
hostB = Host("B")
hostC = Host("C")
hostD = Host("D")
hostA.token = True

# 将四个主机对象存储在一个列表中
hosts = [hostA, hostB, hostC, hostD]

# 让每个主机请求发送一些数据（目标是另一个随机选择的主机）
import random

for host in hosts:
    target = random.choice(hosts)
    while target == host:  # 避免选择自己作为目标
        target = random.choice(hosts)
    host.request(target.name)

# 调用 transmit 函数，模拟网络传输过程（按 Ctrl+C 终止）
transmit(hosts)