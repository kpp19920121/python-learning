import os
from dotenv import load_dotenv, find_dotenv

import requests
from langchain_community.chat_models import ChatOpenAI

# 寻找环境变量的位置
print("开始加载环境变量")
env_filepath = find_dotenv()
print(f"加载环境变量的路径为{env_filepath}")
# 加载环境变量
loadedSuccess = load_dotenv(env_filepath)

print("成功加载环境变量" if loadedSuccess else "未能加载环境变量")

open_api_key = os.getenv("OPENAI_API_KEY")

if not open_api_key:
    raise ValueError("open_api_key不能为空!")

print(f"OPENAI_API_KEY=>{open_api_key}")

from openai import OpenAI





openAIclient = OpenAI(api_key=open_api_key,base_url="https://api.openai.com/")


ChatOpenAI(temperature=0.0)
chatCompletion = openAIclient.chat.completions.create(model="gpt-3.5-turbo", messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "请介绍一下你自己!"}
])




choiceList = chatCompletion.choices

for tempChoice in choiceList:
    print(tempChoice.message)
