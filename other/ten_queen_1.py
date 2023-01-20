# -*- coding = utf-8 -*-
# @TIME :     2023-1-8 下午 12:02
# @Author :   CQUPTLei
# @File :     ten_queen_1.py
# @Software : PyCharm
# @Abstract : 回溯法求N皇后问题
def queen(A, cur=0):
    if cur == len(A):
        print(A)
        return 0
    for col in range(len(A)):  # 遍历当前行的所有位置
        A[cur] = col
        for row in range(cur):  # 检查当前位置是否相克
            if A[row] == col or abs(col - A[row]) == cur - row:
                break
        else:  # 如果完成了整个遍历，则说明位置没有相克
            queen(A, cur+1)  # 计算下一行的位置
queen([None]*4)