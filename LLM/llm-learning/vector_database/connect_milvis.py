import os

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from typing import List
import shutil
import uuid
import tempfile
from langchain.vectorstores import Milvus

from dotenv import  find_dotenv,load_dotenv



from langchain.llms import Ollama


from langchain.document_loaders import Docx2txtLoader


app = FastAPI(redirect_slashes=False)


env_path=find_dotenv()

load_dotenv(env_path)




# 配置静态文件和模板
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

# 全局变量存储向量库
vector_store = None
qa_chain = None

# 连接 Milvus 向量数据库
# Milvus 连接参数（根据你的部署调整 host/port）
milvus_host = os.environ["MILVUS_HOST"]
milvus_port = os.environ["MILVUS_PORT"]
collection_name = os.environ["COLLECTION_NAME"]  # 可自定义

if not milvus_host or not milvus_port or not collection_name:
    raise ValueError("未配置向量数据库的信息!")

print(f"向量数据库的信息为:milvus_host={milvus_host}:milvus_port={milvus_port}:collection_name=>{collection_name}")

#内嵌模型的地址
embdding_module_path=os.environ['LOCAL_EMBEDDING_PATH']

if not embdding_module_path:
    raise ValueError("未配置内嵌模型的地址信息!")


if not os.path.isdir(embdding_module_path):
    raise ValueError("内嵌模型的路径不存在!")




print(f"内嵌模型的路径为:{embdding_module_path}")
#大模型信息
OLLAMA_HOST=os.environ['OLLAMA_HOST']
OLLAMA_MODULE=os.environ['OLLAMA_MODULE']

if not OLLAMA_HOST or not OLLAMA_MODULE:
    raise ValueError("未配置ollama的信息!")

print(f"大模型的信息为:OLLAMA_HOST={OLLAMA_HOST}:OLLAMA_MODULE={OLLAMA_MODULE}")


# 配置嵌入模型
#不使用openai的nlp模型
#embeddings = OpenAIEmbeddings()
embeddings = HuggingFaceEmbeddings(model_name=embdding_module_path)


# 或者使用OpenAI的嵌入模型（需要API key）
# embeddings = OpenAIEmbeddings(openai_api_key="your-api-key")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global vectorstore,qa_chain

    # 保存上传的临时文件
    print("开始上传文件")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(await file.read())
        file_path = tmp.name

    # 使用 Word 文档加载器（任选一种）
    print("使用 Word 文档加载器")
    loader = Docx2txtLoader(file_path)  # 简单格式提取
    # 或
    # loader = UnstructuredWordDocumentLoader(file_path)  # 更复杂但功能更强

    documents = loader.load()
    print("加载文档")

    # 后续处理保持不变...
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)



    # 建立 Milvus 向量存储
    vectorstore = Milvus.from_documents(
        docs,
        embeddings,
        connection_args={"host": milvus_host, "port": milvus_port},
        collection_name=collection_name
    )

    #qa_pipeline = pipeline("text-generation", model="gpt2")  # 示例
    #llm = HuggingFacePipeline(pipeline=qa_pipeline)

    #创建 pipeline（会自动从镜像站下载模型）

    # 方式2：分步加载（更灵活）
    #git clone https://hf-mirror.com/gpt2 gpt2


    llm = Ollama(model=OLLAMA_MODULE,base_url=OLLAMA_HOST)  # 或者 deepseek-coder、llama3 等


    retriever = vectorstore.as_retriever()

    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)


    print("qa_chain=>",qa_chain)

    return {"message": "✅ Word文档已成功上传并构建知识库！"}

@app.post("/ask/")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")

    if not qa_chain:
        return {"answer": "请先上传知识库文档"}

    try:

        print(f"question=>{question}")
        result = qa_chain.run(question)
        return {"answer": result}
    except Exception as e:
        return {"answer": f"发生错误: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)