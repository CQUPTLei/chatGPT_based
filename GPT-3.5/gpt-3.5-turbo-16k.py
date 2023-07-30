#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023-6-21 下午 4:55
# @Author  : CQUPTLEI
# @FileName: gpt-3.5-turbo-16k
# @Software: PyCharm
# @Abstract : 摘要

# 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


import openai
import time
from pathlib import Path
import logging
import requests
from requests.auth import HTTPProxyAuth

proxy_servers = {
    'http': 'http://dahu:11223344@198.52.97.228:37859',
    'https': 'http://dahu:11223344@198.52.97.228:37859'
}

auth = ('dahu', '11223344')

# 设置日志的级别和格式
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

openai.api_key = "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"


class Chat_bot:
    """A chat bot class that can interact with gpt-3.5-turbo-16k model."""

    def __init__(self, model):
        """Initialize the chat bot with some attributes."""
        self.user = "\nYou: "
        self.bot = "GPT-3.5-turbo-16k: "
        self.model = model
        self.question_list = []
        self.answer_list = []
        self.text = ''
        self.turns = []
        self.last_result = ''

    def dialogue_save(self):
        """Save the dialogue content to a markdown file."""
        timestamp = time.strftime("%Y%m%d-%H%M-%S", time.localtime())  # 时间戳
        file_name = 'output/Chat_' + timestamp + '.md'  # 文件名
        f = Path(file_name)
        f.parent.mkdir(parents=True, exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as f:
            for q, a in zip(self.question_list, self.answer_list):
                f.write(f"You: {q}\nGPT-3.5-turbo: {a}\n\n")
        logging.info("对话内容已保存到文件中: " + file_name)

    def Generate(self):
        """Interact with the model and generate responses."""
        logging.info('\n请开始你们的对话，以exit结束。')
        while True:
            # 用户输入
            question = input(self.user)
            self.question_list.append(question)  # 将问题添加到问题列表中
            prompt = self.bot + self.text + self.user + question
            # 退出命令
            if question == 'exit':
                break
            else:
                try:
                    response = requests.post(
                        # 模型名称
                        url="https://api.openai.com/v1/chat/completions",
                        json={
                            "model": self.model,
                            "messages": [
                                # {"role": "system", "content": "You are a helpful assistant."},
                                {"role": "user", "content": prompt},
                                # {"role": "assistant", "content":self.bot }
                            ],
                        },
                        headers={
                            "Authorization": "Bearer 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",
                            "Content-Type": "application/json"
                        },
                        #proxies=proxy_servers,
                       # auth=auth
                    )

                    if response.status_code == 200:
                        # 如果请求成功，获取响应数据中的输出
                        output = response.json()["output"].strip()
                        print(output)
                        self.answer_list.append(output)  # 将回答添加到回答列表中

                        self.last_result = output
                        self.turns += [question] + [output]
                        if len(self.turns) <= 10:
                            self.text = " ".join(self.turns)
                        else:
                            self.text = " ".join(self.turns[-10:])
                    else:
                        # 如果请求失败，显示错误信息
                        logging.error("请求失败：" + response.text)

                # 打印异常
                except Exception as exc:
                    logging.error(exc)
        # 退出对话后保存
        self.dialogue_save()


if __name__ == '__main__':
    bot = Chat_bot('gpt-3.5-turbo-16k')
    bot.Generate()
