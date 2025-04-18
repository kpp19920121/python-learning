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


from langchain.llms import HuggingFacePipeline
from transformers import pipeline, GPT2Tokenizer, GPT2LMHeadModel
from langchain.llms import HuggingFacePipeline



from langchain.llms import Ollama


from langchain.document_loaders import Docx2txtLoader

# 设置使用国内镜像源 (hf-mirror.com)
# 配置国内镜像和缓存路径
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = "./cache"  # 模型缓存目录

app = FastAPI(redirect_slashes=False)




# 配置静态文件和模板
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

# 全局变量存储向量库
vector_store = None
qa_chain = None

module_path="./models/all-MiniLM-L6-v2"


# 配置嵌入模型
embeddings = HuggingFaceEmbeddings(model_name=module_path)

# 连接 Milvus 向量数据库
# Milvus 连接参数（根据你的部署调整 host/port）
milvus_host = "192.168.233.133"
milvus_port = "19530"
collection_name = "langchain_demo"  # 可自定义
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




    #不使用openai的nlp模型
    #embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceEmbeddings(model_name=module_path)

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


    llm = Ollama(model="deepseek-r1:1.5b",base_url="http://192.168.233.133:11434")  # 或者 deepseek-coder、llama3 等


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