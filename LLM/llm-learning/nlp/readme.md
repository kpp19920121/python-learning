# NLP 文本分析助手

一个基于 Flask 的轻量级自然语言处理(NLP)工具，提供关键词提取、情感分析和文本摘要功能。

## 功能特性

- **关键词提取**：使用 KeyBERT 模型提取文本中最相关的5个关键词
- **情感分析**：通过 TextBlob 判断文本情感倾向（积极/消极/中性）
- **文本摘要**：采用 LSA (Latent Semantic Analysis) 算法生成简洁摘要
- **轻量高效**：后端使用 Python Flask，前端简洁易用

## 技术栈

### 后端
- Python 3.x
- Flask (Web框架)
- KeyBERT (关键词提取)
- TextBlob (情感分析)
- Sumy (文本摘要)

### 前端
- HTML5 + Bootstrap 5 (界面)
- Axios (HTTP请求)

## 安装指南

### 前提条件
- Python 3.12.5+
- pip 包管理工具

### 安装步骤

1. 获取源代码
2. 安装依赖

    	pip install flask keybert textblob sumy torch transformers sentence-transformers jieba -i https://pypi.tuna.tsinghua.edu.cn/simple
3. 下载 NLP 模型

		mkdir models
		wget https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/v0.2/all-MiniLM-L6-v2.zip -P models/
		unzip models/all-MiniLM-L6-v2.zip -d models/
## 使用说明
1. 启动服务

		python app.py

2. 访问应用

		打开浏览器访问 http://localhost:5000


3. 输入文本


	- 在文本框中输入任意内容（支持中英文）


	- 点击"分析"按钮
4. 查看结果


	- 关键词列表



	- 情感分析结果



	- 自动生成的摘要
## 项目结构 ##
	F:.                                                              
	│  app.py                                                        
	│  nlp-web-app.iml                                               
	│  readme.md                                                     
	│  test.py                                                       
	│                                                                
	├─models                                                         
	│  └─all-MiniLM-L6-v2                                            
	│          config.json                                           
	│          pytorch_model.bin                                     
	│          sentence_bert_config.json                             
	│          vocab.txt                                             
	│                                                                
	└─templates                                                      
	        index.html  
## 配置选项 ##
###关键词数量设置
kw_model.extract_keywords(text, top_n=5)  # 修改数字调整关键词数量

### 摘要句子数量
summarizer(parser.document, 1)  # 修改数字调整摘要句数
## 常见问题 ##


- 模型下载失败怎么办？

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;手动下载模型包并解压到 models/ 目录,确保模型路径正确



- 中文摘要效果不理想？

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sumy 对中文支持有限，可尝试其他中文分词器



- 如何提高性能？

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;增加 app.run(debug=False)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;考虑使用生产级服务器如 Gunicorn