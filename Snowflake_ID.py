# -*- coding = utf-8 -*-
# @TIME :     2023-1-8 下午 11:50
# @Author :   CQUPTLei
# @File :     Snowflake_ID.py
# @Software : PyCharm
# @Abstract : 产生雪花ID
"""
雪花 ID 是一种用于生成唯一的、有序的 ID 的算法。它由 Twitter 工程师巴里·康奈尔（Barry Kort）在 Twitter 的论文
《Determining the Time from a Snowflake ID》中提出。
雪花 ID 由一个 64 位二进制数字组成，其中包含以下信息：
    41 位时间戳（从某个固定的时刻开始的毫秒数）
    10 位机器标识（用于区分不同机器）
    12 位序列号（用于区分同一机器上生成的 ID）
雪花 ID 的优点包括：
    唯一性：雪花 ID 具有高度的唯一性，即使在高并发的情况下也不会生成相同的 ID。
    有序性：雪花 ID 按照时间戳的顺序生成，因此可以按照生成时间进行排序。
"""

import time

# 起始时间戳（从该时刻开始生成 ID）
START_TS = int(time.mktime(time.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')))
# 机器标识位数
MACHINE_BITS = 10
# 序列号位数
SEQUENCE_BITS = 12
# 机器 ID
machine_id = 1
# 序列号
sequence = 0

# 最大机器 ID（10 位二进制）
MAX_MACHINE_ID = -1 ^ (-1 << MACHINE_BITS)
# 最大序列号（12 位二进制）
MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BITS)

"""
如果当前时间戳小于上一次生成 ID 的时间戳，说明时钟发生了回拨，此时会抛出一个 ValueError 异常。
如果当前时间戳等于上一次生成 ID 的时间戳，则会增加序列号，并判断序列号是否达到最大值.
"""
def generate_id():
    global machine_id, sequence
    last_ts = 1111111111111  #旧ID，这里暂时没有使用
    current_ts = int(time.time() * 1000)
    if current_ts < last_ts:
        raise ValueError('时钟回拨')
    if current_ts == last_ts:
        sequence = (sequence + 1) & MAX_SEQUENCE
        if sequence == 0:
            raise ValueError('毫秒内序列号溢出')
    else:
        sequence = 0
    last_ts = current_ts

    new_id = ((current_ts - START_TS) << (MACHINE_BITS + SEQUENCE_BITS)) | (machine_id << SEQUENCE_BITS) | sequence
    return new_id
if __name__ == '__main__':
    print(generate_id())