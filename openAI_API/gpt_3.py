# -*- coding = utf-8 -*-
# @TIME :     2023-2-21 下午 9:47
# @Author :   CQUPTLei
# @File :     gpt_3.py
# @Software : PyCharm
# @Abstract : GPT-3的简单使用，不支持上下文连续对话，自己申请API key，很简单哈。

import openai
openai.api_key = "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"

class Chat_bot:
    def __init__(self,model):
        self.user = "\nYou: "
        self.bot = "GPT-3: "
        # 具体的GPT-3模型名称
        self.model = model

    def Generate(self):
        while True:
            # 用户输入
            prompt = input(self.user)
            # 退出命令
            if prompt == 'exit':
                break
            else:
                try:
                    response = openai.Completion.create(
                        # 模型名称
                        model= self.model,
                        # 用户提供的输入文本，用于指导GPT输出
                        prompt=prompt,
                        # 控制输出的多样性，0-1，其中0表示最保守的输出，1表示最多样化的输出。
                        temperature=0,
                        # 输出的最大长度（输入+输出的token不能大于模型的最大token）,可以动态调整
                        max_tokens=1500,
                        # [控制字符的重复度] -2.0 ~ 2.0 之间的数字，正值会根据新 tokens 在文本中的现有频率对其进行惩罚，从而降低模型逐字重复同一行的可能性
                        frequency_penalty=0.2,
                        # [控制主题的重复度] -2.0 ~ 2.0 之间的数字，正值会根据到目前为止是否出现在文本中来惩罚新 tokens，从而增加模型谈论新主题的可能性
                        presence_penalty=0.15,
                    )
                    # print(self.bot,response)
                    print(self.bot, response["choices"][0]["text"].strip())
                # 打印异常
                except Exception as exc:
                    print(exc)

if __name__ =='__main__':
    bot = Chat_bot('text-davinci-003')
    bot.Generate()