# -*- coding = utf-8 -*-
# @TIME :     2023-4-7 下午 5:23
# @Author :   CQUPTLei
# @File :     GPT_3.5_Turbo.py
# @Software : PyCharm
# @Abstract :
# fR9&&*P7!8fUtjx
import openai
import time
from pathlib import Path
from requests.auth import HTTPProxyAuth

proxy_servers = {
    'http': 'http://198.52.97.228:37859',
    'https': 'http://198.52.97.228:37859'
}

auth = ('dahu', '11223344')

openai.api_key = "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"


class Chat_bot:
    def __init__(self,model):
        self.user = "\nYou: "
        self.bot = "GPT-3.5-turbo-16k: "
        self.model = model
        self.question_list = []
        self.answer_list = []
        self.text = ''
        self.turns = []
        self.last_result = ''

    def dialogue_save(self):
        timestamp = time.strftime("%Y%m%d-%H%M-%S", time.localtime())  # 时间戳
        file_name = 'output/Chat_' + timestamp + '.md'  # 文件名
        f = Path(file_name)
        f.parent.mkdir(parents=True, exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as f:
            for q, a in zip(self.question_list, self.answer_list):
                f.write(f"You: {q}\nGPT-3.5-turbo: {a}\n\n")
        print("对话内容已保存到文件中: " + file_name)

    def Generate(self):
        print('\n请开始你们的对话，以exit结束。')
        while True:
            # 用户输入
            question = input(self.user)
            self.question_list.append(question) # 将问题添加到问题列表中
            prompt = self.bot + self.text  + self.user + question
            # 退出命令
            if question == 'exit':
                break
            else:
                try:
                    response = openai.ChatCompletion.create(
                        # 模型名称
                        model= self.model,
                        messages=[
                            # {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": prompt},
                            # {"role": "assistant", "content":self.bot }
                        ],
                    )

                    result = response["choices"][0]["message"]["content"].strip()
                    print(result)
                    self.answer_list.append(result) #将回答添加到回答列表中

                    self.last_result = result
                    self.turns += [question] + [result]
                    if len(self.turns) <= 10:
                        self.text = " ".join(self.turns)
                    else:
                        self.text = " ".join(self.turns[-10:])

                # 打印异常
                except Exception as exc:
                    print(exc)
        # 退出对话后保存
        self.dialogue_save()

if __name__ =='__main__':
    bot = Chat_bot('gpt-3.5-turbo-16k')
    bot.Generate()
