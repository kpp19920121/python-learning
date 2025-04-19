文本智能分析服务

# 1.项目结构 #
	├─nlp
	│  │  app.py
	│  │  templates  
	│  │  readme.md
- app.py

	主程序。 

- templates

	web的模板页面
	
# 2.核心功能 #
## 2.1关键词提取 ##


- 基于KeyBERT模型提取文本核心关键词



- 使用本地预训练模型all-MiniLM-L6-v2（384维）



- 返回Top 5最具代表性关键词



- 完全离线运行，无需API调用

## 2.2情感分析 ##


- 采用TextBlob进行情感极性检测



- 输出结果：



	- 情感倾向（积极/消极/中性）



	- 极性得分（-1到1区间）

## 2.3自动文本摘要 ##


- 基于LSA（潜在语义分析）算法



- 支持中文文本处理（使用中文tokenizer）



- 可配置摘要句子数量

# 3.技术栈 #



## 3.1后端 ##


	- Python 3.x


	- Flask (Web框架)


	- KeyBERT (关键词提取)


	- TextBlob (情感分析)


	- Sumy (文本摘要)


## 3.2前端 ##


	- HTML5 + Bootstrap 5 (界面)


	- Axios (HTTP请求)

# 4.环境配置 #
## 4.1依赖安装 ##

	pip install flask keybert textblob sumy sentence-transformers



- flask:
轻量级Python Web框架，用于快速构建API服务（提供HTTP接口）。



- keybert:
关键词提取工具，基于BERT模型从文本中自动提取核心关键词。



- textblob:
简单的情感分析库，支持情感极性检测（判断积极/消极/中性）。



- sumy:
文本摘要生成工具，内置LSA/LexRank等算法，支持多语言。



- sentence-transformers:
文本嵌入模型框架，可将文本转换为向量表示（如all-MiniLM-L6-v2模型）。

##4.2关键参数配置 ##
		
		#使用内嵌的embdding模型，配置模型文件路径开始
		LOCAL_EMBEDDING_PATH="D:/software/AI/modules/all-MiniLM-L6-v2"
		

- 启动服务

		python app.py

- 默认访问地址：
	- http://localhost:5000

# 5.接口说明 #


- 请求示例

		POST /analyze
		Content-Type: application/json
		
		{
		    "text": "要分析的文本内容..."
		}
		响应示例
		json
		{
		    "keywords": ["关键词1", "关键词2"],
		    "sentiment": "积极",
		    "summary": "文本摘要内容..."
		}
# 6.扩展建议 #


- 性能优化：添加缓存机制（如Redis）存储高频分析结果



- 功能增强：集成实体识别或主题建模



- 部署方案：使用Docker容器化打包模型和服务



- 注：首次运行时会自动初始化模型，请确保./models目录有写入权限