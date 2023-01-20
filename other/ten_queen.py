# -*- coding = utf-8 -*-
# @TIME :     2023-1-8 上午 11:44
# @Author :   CQUPTLei
# @File :     ten_queen.py
# @Software : PyCharm
# @Abstract : A*算法求解10皇后
import sys
import heapq

# 棋盘的大小
N = 10

# 定义棋盘
board = [[0] * N for _ in range(N)]

# 定义目标节点
end = (0, 0)

# 定义曼哈顿距离函数
# 曼哈顿距离：两点在东西方向的距离加上南北方向的距离
# 使用曼哈顿距离只有加减运算，计算代价更低
def manhattan(pos):
    x, y = pos
    ex, ey = end
    return abs(x - ex) + abs(y - ey)

# 定义节点类
class Node:
    def __init__(self, pos, queens, cost):
        self.pos = pos
        self.queens = queens
        self.cost = cost
        self.f = cost + manhattan(pos)

    # 定义比较函数，用于堆排序
    def __lt__(self, other):
        return self.f < other.f

# 定义搜索函数
def astar(start):
    # 初始化开放列表和关闭列表
    open_list = []
    close_list = set()

    # 将起点加入开放列表
    heapq.heappush(open_list, start)

    # 循环扩展节点
    while open_list:
        # 从开放列表中取出 F 值最小的节点
        node = heapq.heappop(open_list)

        # 将节点加入关闭列表
        close_list.add(node.pos)

        # 如果节点为目标节点，返回解
        if node.pos == end:
            return node.queens

        # 遍历周围的节点
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        #计算新的坐标
            x, y = node.pos
            x, y = x + dx, y + dy
        # 越界或在关闭列表中，跳过
        if not (0 <= x < N and 0 <= y < N) or (x, y) in close_list:
            continue

        # 计算新的皇后布局
        queens = node.queens[:]
        queens.add((x, y))

        # 创建新的节点
        new_node = Node((x, y), queens, node.cost + 1)

        # 将新节点加入开放列表
        heapq.heappush(open_list, new_node)

    # 找不到解
    return None
# 初始化起点
start = Node((0, 0), {(0, 0)}, 0)

# 调用搜索函数
result = astar(start)

# 输出结果
if result:
    for x, y in result:
        board[x][y] = 1
        for row in board:
            print(row)
else:
    print("No solution.")