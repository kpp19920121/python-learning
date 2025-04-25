from sentence_transformers import SentenceTransformer

import sys,os

import requests
import json



from dotenv import load_dotenv,find_dotenv

from local_embedding import LocalEmbedding
from wenXinYiYan_embedding import  WenXinYiYanEmbedding

env_path=find_dotenv()

env_load_success=load_flag=load_dotenv(env_path)

if not env_load_success:
    raise ValueError("加载配置文件报错!")


def test_local_embedding():
    local_embedding_path=os.environ['LOCAL_EMBEDDING_PATH']


    if  not os.path.isdir(local_embedding_path):
        raise ValueError(f"模型路径{local_embedding_path}不存在，请检查后重试!")

    model = SentenceTransformer(local_embedding_path)


    embeddings = model.encode(sentences="要生成 embedding 的输入文本，字符串形式。")


    for tempembedding in embeddings :
        print(f"{tempembedding}")


def _get_wenxin_token()->str:

    """
    官方文档:https://cloud.baidu.com/doc/WENXINWORKSHOP/s/dlv4pct3s
    根据步骤一获取的API Key、Secret Key，获取access_token。参考以下获取access_token，更多详情方法请参考获取access_token。
    注意：access_token默认有效期30天，生产环境注意及时刷新。
    :return:
    """

    wenxin_api_key=os.environ["WENXIN_API_KEY"];
    wenxin_secret_key=os.environ["WENXIN_SECRET_KEY"]


    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(wenxin_api_key,wenxin_secret_key)
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)


    return str(response.json().get("access_token"))

def test_wenxin_embedding():

    token=_get_wenxin_token();

    headers = {
        'Content-Type': 'application/json',
        'appid': ''
    }

    print(f"headers=>{headers}")


    payload = json.dumps({
        "model": "tao-8k",
        "input": [
            "你是谁"
        ]
    })

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/embedding-v1?access_token=" + _get_wenxin_token()
    response=requests.request("POST",url,headers=headers, data=payload.encode("utf-8"))



    print(str(response.json()))

    for temData in response.json().get("data"):
        for tempData1 in temData.get("embedding"):
            print(tempData1)

if __name__=='__main__':
    #test_local_embedding();
    #test_wenxin_embedding();
    #print(_get_wenxin_token())
    #embddings=LocalEmbedding(os.environ['LOCAL_EMBEDDING_PATH'])
    embddings=WenXinYiYanEmbedding(os.environ['WENXIN_API_KEY'],os.environ['WENXIN_SECRET_KEY'])

    float_list=embddings.embed_documents(["我是谁"]);


    print("===============embed_documents开始==========================")
    for tempData in float_list:
        print(str(tempData))
    print("===============embed_documents结束==========================")


    print("===============embed_query开始==========================")

    for tempData in embddings.embed_query("我是谁?"):
         print(str(tempData))

    print("===============embed_query结束==========================")
