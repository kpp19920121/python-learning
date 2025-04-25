from typing import List
from langchain_core.embeddings import Embeddings  # LangChain 的嵌入接口基类
from sentence_transformers import SentenceTransformer  # 用于加载本地 embedding 模型


class LocalEmbedding(Embeddings):

    """
    一个自定义的本地嵌入模型类，用于将文本转换为向量，兼容 LangChain 的 Embeddings 接口
    """

    def __init__(self, model_path: str) -> None:
        """
        初始化本地嵌入模型

        :param model_path: 本地模型的路径或模型名称，必须是已下载好的 SentenceTransformer 模型
        """
        self.model = SentenceTransformer(model_path)  # 加载本地模型

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        对多个文档进行向量化，用于向量数据库中的文档嵌入

        :param texts: 文本列表，每个元素表示一个文档片段
        :return: 对应的嵌入向量列表，每个向量是 float 数值组成的 list
        """
        # encode() 方法将文本转换为嵌入向量，convert_to_numpy=True 返回 numpy 数组
        # .tolist() 转换为 Python 的 list 格式，便于后续处理
        return self.model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        对查询语句进行向量化，用于匹配文档库中的嵌入向量

        :param text: 查询语句（用户输入的问题或关键词）
        :return: 查询语句对应的嵌入向量
        """
        # 直接调用 embed_documents 来处理单个文本，并取返回结果的第一个向量
        return self.embed_documents([text])[0]


