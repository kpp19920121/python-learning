from typing import List, Dict
from langchain_core.embeddings import Embeddings  # LangChain 的嵌入接口基类
from overrides import overrides
from sentence_transformers import SentenceTransformer  # 用于加载本地 embedding 模型
import requests,json

class WenXinYiYanEmbedding(Embeddings):

    """
    一个自定义的本地嵌入模型类，用于将文本转换为向量，兼容 LangChain 的 Embeddings 接口
    """

    def _get_wenxin_token(self)->str:

        """
        官方文档:https://cloud.baidu.com/doc/WENXINWORKSHOP/s/dlv4pct3s
        根据步骤一获取的API Key、Secret Key，获取access_token。参考以下获取access_token，更多详情方法请参考获取access_token。
        注意：access_token默认有效期30天，生产环境注意及时刷新。
        :return:
        """


        url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(
            self.wenxin_api_key, self.wenxin_secret_key)
        payload = json.dumps("")
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)


        return str(response.json().get("access_token"))


    def _wenxin_embedding(self,text_list :list[str])->list[list[float]]:

        token=self._get_wenxin_token();

        headers = {
            'Content-Type': 'application/json',
            'appid': ''
        }

        print(f"headers=>{headers}")


        payload = json.dumps({
            "model": "tao-8k",
            "input": text_list
        })

        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token=" + self._get_wenxin_token()
        response=requests.request("POST",url,headers=headers, data=payload.encode("utf-8"))

        data_dict_list=response.json().get("data");

        return [tempData['embedding'] for tempData in data_dict_list]



    def __init__(self, wenxin_api_key:str,wenxin_secret_key:str) -> None:
        """
        初始化本地嵌入模型

        :param model_path: 本地模型的路径或模型名称，必须是已下载好的 SentenceTransformer 模型
        """
        self.wenxin_api_key = wenxin_api_key
        self.wenxin_secret_key=wenxin_secret_key

    @overrides
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        对多个文档进行向量化，用于向量数据库中的文档嵌入

        :param texts: 文本列表，每个元素表示一个文档片段
        :return: 对应的嵌入向量列表，每个向量是 float 数值组成的 list
        """
        # encode() 方法将文本转换为嵌入向量，convert_to_numpy=True 返回 numpy 数组
        # .tolist() 转换为 Python 的 list 格式，便于后续处理


        return self._wenxin_embedding(texts)
        #return self.model.encode(texts, convert_to_numpy=True).tolist()

    @overrides
    def embed_query(self, text: str) -> List[float]:
        """
        对查询语句进行向量化，用于匹配文档库中的嵌入向量

        :param text: 查询语句（用户输入的问题或关键词）
        :return: 查询语句对应的嵌入向量
        """
        # 直接调用 embed_documents 来处理单个文本，并取返回结果的第一个向量


        return self._wenxin_embedding([text])[0]


