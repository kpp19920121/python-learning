#1.项目结构  #
	├─vector_database
	│  │  app.py
	│  │  connect_milvis.py 
	│  │  find_files.py
	│  │  readme.md


- connect_milvis.py

	FastAPI应用，模拟知识库问答。 

# 2.功能特性 #
## connect_milvis.py ##


- 文档处理：



	- 支持上传Word文档(.docx)



	- 自动进行文本分块处理



- 向量存储：



	- 使用HuggingFace的MiniLM嵌入模型



	- 集成Milvus向量数据库存储



	- 支持自定义集合(collection)名称



- 问答系统：



	- 基于Ollama本地大模型(deepseek-r1)



	- 实现检索增强生成(RAG)功能

# 3.配置要求 #
## 3.1环境依赖 ##


- Python 3.11+



- Milvus 2.0+ (已部署)



- Ollama服务 (已部署)

## 3.2关键参数配置 ##

		# Milvus连接配置
		milvus_host = "192.168.233.133"  # 修改为你的Milvus地址
		milvus_port = "19530"            # Milvus端口
		
		# Ollama配置
		ollama_url = "http://192.168.233.133:11434"  # Ollama服务地址
		ollama_model = "deepseek-r1:1.5b"            # 使用的模型
# 4.安装与运行 #
## 安装依赖 ##

	pip install langchain_community sentence-transformers jinja2 python-multipart fastapi docx2txt uvicorn langchain milvus pymilvus python-docx -i https://pypi.tuna.tsinghua.edu.cn/simple



- 

- langchain_community：LangChain 社区扩展包，集成更多外部工具与数据源。



- sentence-transformers：用于文本向量化，支持语义搜索与文本匹配。



- jinja2：Python 的模板引擎，用于动态生成文本内容。



- python-multipart：支持 FastAPI 等框架处理 multipart/form-data 上传。



- fastapi：现代、快速的 Python Web 框架，适合构建 API 服务。



- docx2txt：提取 .docx 文件中的纯文本内容。



- uvicorn：ASGI 服务器，用于运行 FastAPI 等异步 Web 应用。



- langchain：构建 LLM 应用的核心框架，支持各种链、代理与工具集成。



- milvus：开源向量数据库，支持大规模相似度搜索。



- pymilvus：Python 客户端，用于连接和操作 Milvus 数据库。



- python-docx：用于创建、修改 .docx Word 文件。

## 启动服务： ##

	python connect_milvus.py
## 访问接口 ##



- 前端页面：http://localhost:8000



- 上传接口：POST /upload



- 问答接口：POST /ask/

# 5.扩展说明 #


- 模型替换：



	- 可更换为其他HuggingFace嵌入模型



	- 支持切换为OpenAI的嵌入模型(需API key)

- 未来扩展：



	- 计划添加PDF/TXT文件支持



	- 将增加多集合管理功能



	- 考虑集成更多本地大模型

# 6.使用示例 #


- 上传文档：


		curl -X POST -F "file=@example.docx" http://localhost:8000/upload



- 提问测试：


		curl -X POST -H "Content-Type: application/json" -d '{"question":"文档主要内容是什么？"}' http://localhost:8000/ask/
# 7.注意事项 #


- 首次运行会自动下载嵌入模型(约80MB)



- 确保Milvus和Ollama服务已正确启动



- 生产环境建议添加身份验证机制


