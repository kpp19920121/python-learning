import os,sys

from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

# 假设 vector_database 是你项目的子目录
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import vector_database.connect_chroma_demo as connect_chroma_demo

from  langchain_community.chat_models.ollama import ChatOllama

#1.搜索和加载向量数据库中的document
documetn_list=connect_chroma_demo.chroma_similarity_search("redis")

vector_db=connect_chroma_demo.get_vectordb();

#2.创建llm
base_chatModel=ChatOllama(model="qwen:1.8b",base_url="http://192.168.233.133:11434")




def  answer_1(message:str):

    """检索问答链

    :param message: 检索内容
    :return:
    """


    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    """

    QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context","question"],
                                     template=template)

    qa_chain =RetrievalQA.from_chain_type(
        llm=base_chatModel,
        retriever=vector_db.as_retriever(),
        chain_type_kwargs={"prompt":QA_CHAIN_PROMPT}
    )

    result =qa_chain.invoke({"query": message})
    #result = qa_chain({"query": "什么是南瓜书？"})
    print("大模型+知识库后回答 question_1 的结果：")
    print(result["result"])


def  answer_2(message:str):
    """带记忆的检索问答链

    :param message: 检索内容
    :return:
    """
    template = """使用以下上下文来回答最后的问题。如果你不知道答案，就说你不知道，不要试图编造答
    案。最多使用三句话。尽量使答案简明扼要。总是在回答的最后说“谢谢你的提问！”。
    {context}
    问题: {question}
    """

    memory = ConversationBufferMemory(
        memory_key="chat_history",  # 与 prompt 的输入变量保持一致。
        return_messages=True  # 将以消息列表的形式返回聊天记录，而不是单个字符串
    )


    qa_chain=ConversationalRetrievalChain.from_llm(
        llm=base_chatModel,
        retriever=vector_db.as_retriever(),
        memory=memory
    )

    result =qa_chain.invoke({"question": message})
    #result = qa_chain({"query": "什么是南瓜书？"})
    print("大模型+知识库后回答 question_1 的结果：")
    print(result["answer"])


if __name__=='__main__':
    answer_2("请介绍nginx的高可用，不超过300字")
    print("======================================================")
    answer_2("请描述一下具体怎么安装？？")

