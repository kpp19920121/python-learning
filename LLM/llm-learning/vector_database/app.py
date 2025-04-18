import sys,os
from sentence_transformers import SentenceTransformer

from  langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from vector_database import find_files



#1.加载文档
documents=find_files.get_documents("F:/repository/git_repository/document/运维")

#2.构建embedding
model = SentenceTransformer('../models/all-MiniLM-L6-v2')
embeddings = model.encode(sentences="要生成 embedding 的输入文本，字符串形式。")


#3.分词，把大的文档进行拆分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50)

split_docs = text_splitter.split_documents(documents)


#3.写入向量数据库

#定义持久化路径
persist_directory = '../../data_base/vector_db/chroma'

vectordb = Chroma.from_documents(
    documents=split_docs, # 为了速度，只选择前 20 个切分的 doc 进行生成；使用千帆时因QPS限制，建议选择前 5 个doc
    embedding=embeddings,
    persist_directory=persist_directory  # 允许我们将persist_directory目录保存到磁盘上
)


vectordb.persist


