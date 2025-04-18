import os

import ollama
from dotenv import load_dotenv, find_dotenv

from ollama import Client,chat


def initollama():
    envPath = find_dotenv(".env")
    flag = load_dotenv(envPath);
    if not flag:
        raise ValueError("加载环境变量错误!")
    client = Client(host=os.getenv("OLLAMA_HOST"))
    return client



def chatwithollama(requestmessage,stream=False):
    client = initollama()

    if not client:
        raise ValueError("初始化错误!")

    response = client.chat(model="deepseek-r1:1.5b", messages=[{
        'role': 'user',
        'content': f'{requestmessage}'
    }],stream=stream)

    if not response:
        raise ValueError("返回对象不能为空!")

    return response;





print("使用一次性回复:")

response = chatwithollama("你是谁?")

print(f"responseContent=>{response.message.content}")


print("使用流回复:")
streamContent=chatwithollama("你是谁",True)

for chunk in streamContent:
    print(chunk.message.content,end='',flush=True)

response=chatwithollama("请生成包括书名、作者和类别的三本虚构的、非真实存在的中文书籍清单,",True)



for chunk in response:
    print(chunk.message.content,end='',flush=True)
