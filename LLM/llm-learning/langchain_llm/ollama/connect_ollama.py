import os
from typing import Union, Iterator

import ollama
from dotenv import load_dotenv, find_dotenv
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

from ollama import Client, chat, ChatResponse

from langchain.prompts.chat import ChatPromptTemplate

def initollama():
    envPath = find_dotenv(".env")
    flag = load_dotenv(envPath);
    if not flag:
        raise ValueError("加载环境变量错误!")
    client = Client(host=os.getenv("OLLAMA_HOST"))
    return client



def chatwithollama(requestmessage:str,stream=False)->Union[ChatResponse, Iterator[ChatResponse]]:
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


def chat_test():
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


def get_chatPromptTemplate()->list[BaseMessage]:
    template = "你是一个翻译助手，可以帮助我将 {input_language} 翻译成 {output_language}."
    human_template = "{text}"
    chatPromptTemplate=ChatPromptTemplate([
    ("system", template),
    ("human", human_template),
    ])
    text = "我带着比身体重的行李，\
    游入尼罗河底，\
    经过几道闪电 看到一堆光圈，\
    不确定是不是这里。\
    "

    messages  = chatPromptTemplate.format_messages(input_language="中文", output_language="英文", text=text)


    print(messages)

    return messages;








if __name__=="__main__":
    chat_test()

