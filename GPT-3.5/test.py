# 导入openai库
import openai

# 设置API密钥
openai.api_key = "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"

# 定义一个函数，用于调用gpt-3.5-turbo-16k模型
def chat_with_gpt35turbo16k(prompt, functions=None, function_call=None):
  # 使用Chat Completions API发送请求
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613", # 指定模型为gpt-3.5-turbo-16k
    messages=[{"role": "user", "content": prompt}], # 将用户输入作为消息
    functions=functions, # 如果有定义函数，传入函数列表
    function_call=function_call # 如果有指定函数调用，传入函数调用对象
  )
  # 返回模型的回复内容或函数调用对象
  if response.choices[0].message.function_call:
    return response.choices[0].message.function_call
  else:
    return response.choices[0].message.content

# 定义一个函数，用于获取当前天气
def get_current_weather(location, unit="celsius"):
  # 使用某个第三方API查询天气（这里只是示意）
  weather = openai.WeatherAPI.query(location, unit)
  # 返回天气信息的JSON对象
  return {"temperature": weather.temperature, "unit": unit, "description": weather.description}

# 定义一个函数，用于发送邮件（这里只是示意）
def send_email(to, body):
  # 使用某个第三方API发送邮件（这里只是示意）
  email = openai.EmailAPI.send(to, body)
  # 返回邮件发送状态的JSON对象
  return {"status": email.status, "message": email.message}

# 定义一个列表，包含所有可用的函数
functions = [
  {
    "name": "get_current_weather",
    "description": "Get the current weather in a given location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "The city and state, e.g. San Francisco, CA"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    }
  },
  {
    "name": "send_email",
    "description": "Send an email to a given recipient",
    "parameters": {
      "type": "object",
      "properties": {
        "to": {
          "type": "string",
          "description": "The email address of the recipient"
        },
        "body": {
          "type": "string",
          "description": "The content of the email"
        }
      },
      "required": ["to", "body"]
    }
  }
]

# 初始化一个空的函数调用对象
function_call = None

# 初始化一个空的对话历史列表
dialogue_history = []

# 开始与模型对话
while True:
  # 获取用户输入
  prompt = input("User: ")
  # 如果用户输入"quit"，退出对话
  if prompt.lower() == "quit":
    break
  # 将用户输入添加到对话历史列表
  dialogue_history.append({"role": "user", "content": prompt})
  # 调用gpt-3.5-turbo-16k模型，传入用户输入，函数列表和函数调用对象
  reply = chat_with_gpt35turbo16k(prompt, functions, function_call)
  # 如果回复是一个函数调用对象
  if isinstance(reply, dict) and "name" in reply and "arguments" in reply:
    # 获取函数的名称和参数
    function_name = reply["name"]
    function_arguments = eval(reply["arguments"])
    # 根据函数的名称，调用相应的本地函数，并传入参数
    if function_name == "get_current_weather":
      result = get_current_weather(**function_arguments)
    elif function_name == "send_email":
      result = send_email(**function_arguments)
    else:
      result = None
    # 如果有返回结果，将其作为函数的回复内容，否则返回一个错误信息
    if result:
      function_content = str(result)
    else:
      function_content = "Error: Invalid function name or arguments."
    # 将函数的回复内容添加到对话历史列表
    dialogue_history.append({"role": "function", "name": function_name, "content": function_content})
    # 将函数的回复内容作为新的函数调用对象，传入模型，以便模型进行总结或后续操作
    function_call = {"name": function_name, "content": function_content}
    # 调用gpt-3.5-turbo-16k模型，传入空字符串，函数列表和函数调用对象，获取模型的总结或后续操作
    summary = chat_with_gpt35turbo16k("", functions, function_call)
    # 如果总结是一个字符串，将其作为模型的回复内容，否则返回一个错误信息
    if isinstance(summary, str):
      reply_content = summary
    else:
      reply_content = "Error: Invalid summary."
    # 将模型的回复内容添加到对话历史列表
    dialogue_history.append({"role": "assistant", "content": reply_content})
    # 打印模型的回复内容
    print("Assistant:", reply_content)
  # 如果回复是一个字符串，将其作为模型的回复内容
  elif isinstance(reply, str):
    reply_content = reply
    # 将模型的回复内容添加到对话历史列表
    dialogue_history.append({"role": "assistant", "content": reply_content})
    # 打印模型的回复内容
    print("Assistant:", reply_content)
  # 否则，返回一个错误信息，并退出对话
  else:
    print("Error: Invalid reply.")
    break

