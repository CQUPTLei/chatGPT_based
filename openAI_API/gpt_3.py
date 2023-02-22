# -*- coding = utf-8 -*-
# @TIME :     2023-2-21 下午 9:47
# @Author :   CQUPTLei
# @File :     gpt_3.py
# @Software : PyCharm
# @Abstract : GPT-3的简单使用，自己申请API key，很简单哈。

import openai
openai.api_key = "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"

class Chat_bot:
    def __init__(self,type):
        self.user = "\nYou: "
        self.bot = "GPT-3: "
        # 具体的GPT-3模型名称
        self.type = type

    def Generate(self):
        while True:
            prompt = input(self.user)
            if prompt == 'exit':
                break
            else:
                try:
                    response = openai.Completion.create(
                        # 模型名称
                        model= self.type,
                        # 用户提供的输入文本，用于指导GPT输出
                        prompt=prompt,
                        # 控制输出的多样性，0-1，其中0表示最保守的输出，1表示最多样化的输出。
                        temperature=0,
                        # 输出的最大长度（输入+输出的token不能大于模型的最大token）
                        max_tokens=1500,
                        frequency_penalty=0.0,
                        presence_penalty=0.0,
                    )
                    print(self.bot, response["choices"][0]["text"].strip())
                except Exception as exc:
                    print(exc)

if __name__ =='__main__':
    bot = Chat_bot('text-davinci-003')
    bot.Generate()