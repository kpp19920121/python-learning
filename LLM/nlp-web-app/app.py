from flask import Flask, render_template, request, jsonify
from keybert import KeyBERT
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# 创建 Flask 应用
app = Flask(__name__)

# 初始化关键词提取模型（离线模式）
# KeyBERT 通过下载模型，通常会在首次使用时缓存模型。使用 `local_files_only=True` 以避免再次尝试下载。
module_path="./models/all-MiniLM-L6-v2"
kw_model = KeyBERT(model=module_path)  # 指定一个本地可用模型名称

# 初始化文本摘要器（LSA算法）
summarizer = LsaSummarizer()

# 首页路由，返回前端页面
@app.route('/')
def index():
    return render_template('index.html')

# 分析文本的接口，POST 请求
@app.route('/analyze', methods=['POST'])
def analyze():
    # 从前端获取传来的 JSON 数据
    text = request.json.get('text')

    # 1️⃣ 关键词提取
    keywords = [kw[0] for kw in kw_model.extract_keywords(text, top_n=5)]

    print(f"输入的关键词:",keywords)

    # 2️⃣ 情感分析（英文效果最佳）
    blob = TextBlob(text)
    print("blob=>",blob)


    polarity = blob.sentiment.polarity  # 得到情感倾向得分（-1 ~ 1）
    sentiment = "积极" if polarity > 0 else "消极" if polarity < 0 else "中性"

    # 3️⃣ 文本摘要（提取一段总结）
    parser = PlaintextParser.from_string(text, Tokenizer("chinese"))  # 中文切分器
    summary = "".join([str(s) for s in summarizer(parser.document, 1)])  # 抽取一句摘要

    # 把分析结果打包为 JSON 返回
    return jsonify({
        'keywords': keywords,
        'sentiment': sentiment,
        'summary': summary
    })

# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)
