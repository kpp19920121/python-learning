import sys,os
from typing import List

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from sentence_transformers import SentenceTransformer

from  langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter


from  dotenv import  find_dotenv,load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from vector_database import find_files


from embedding.local_embedding import LocalEmbedding
env_path=find_dotenv()

load_dotenv(env_path)




#2.构建embedding
module_path=os.environ['LOCAL_EMBEDDING_PATH']

#embeddings =LocalEmbedding(module_path)
embeddings=LocalEmbedding("D:/models/all-MiniLM-L6-v2")


vectordb=None

#定义持久化路径
persist_directory = os.getenv('PERSIST_DIRECTORY')


def  persist_data():

    #1.加载文档
    document_root_path=os.environ['DOCUMENT_ROOT_PATH']
    documents=find_files.get_documents(document_root_path)


    #3.分词，把大的文档进行拆分
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50)

    split_docs = text_splitter.split_documents(documents)

#3.写入向量数据库



    print(f"开始持久化数据库:"+os.path.abspath(persist_directory))

    vectordb = Chroma.from_documents(
        documents=split_docs, # 为了速度，只选择前 20 个切分的 doc 进行生成；使用千帆时因QPS限制，建议选择前 5 个doc
        embedding=embeddings,
        persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
    )

    #持久化数据库
    vectordb.persist
    print("向量库中存储的数量:"+str(vectordb._collection.count()))



def get_vectordb()->VectorStore:
    vectordb = Chroma(
        persist_directory=persist_directory,  # 必须与保存时相同
        embedding_function=embeddings  # 需要提供相同的embedding模型
    )

    return vectordb;



#相似度检索
""""""
def chroma_similarity_search(content :str) -> List[Document]:


    """
    :param content: 待检索的内容
    :return:
    当你需要数据库返回严谨的按余弦相似度排序的结果时可以使用similarity_search函数。
    """

    print("==========开始连接向量数据库============")


    vectordb =get_vectordb()
    print("==========开始使用相似度检索============")

        #数据库检索:similarity_search
    doc_list=vectordb.similarity_search(content,4)

    if not doc_list:
        raise ValueError("未检索到相关内容!")

    for  index,sim_doc  in enumerate(doc_list):
        print(f"检索到的第{index}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")


#相似度检索
""""""
def chroma_mmr_search(content :str):


    """
    :param content: 待检索的内容
    :return:
    当你需要数据库返回严谨的按余弦相似度排序的结果时可以使用similarity_search函数。
    """

    print("==========开始连接向量数据库============")

    vectordb = Chroma(
        persist_directory=persist_directory,  # 必须与保存时相同
        embedding_function=embeddings  # 需要提供相同的embedding模型
    )
    print("==========开始使用相似度检索============")

        #数据库检索:similarity_search
    doc_list=vectordb.max_marginal_relevance_search(content,4)

    if not doc_list:
        raise ValueError("未检索到相关内容!")

    for  index,sim_doc  in enumerate(doc_list):
        print(f"检索到的第{index}个内容: \n{sim_doc.page_content[:200]}", end="\n--------------\n")



if __name__ == "__main__":
    #chroma_similarity_search("redis");
    chroma_mmr_search("redis")
