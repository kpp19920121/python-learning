
import json
import requests

wenxin_api_key="MePVFOYERboTTXjCVpba6zlc"
wenxin_secret_key="I57mM2OUyQqDzjDJnqA6swImm3PvXkjU"


def _get_wenxin_token()->str:

    """
    官方文档:https://cloud.baidu.com/doc/WENXINWORKSHOP/s/dlv4pct3s
    根据步骤一获取的API Key、Secret Key，获取access_token。参考以下获取access_token，更多详情方法请参考获取access_token。
    注意：access_token默认有效期30天，生产环境注意及时刷新。
    :return:
    """


    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}".format(
        wenxin_api_key, wenxin_secret_key)
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)


    return str(response.json().get("access_token"))



token=_get_wenxin_token();

print(f"token=>{_get_wenxin_token()}")

headers = {
    'Content-Type': 'application/json',
    'appid': ''
}

print(f"headers=>{headers}")

documents = [
    "Python是一种高级编程语言，适合初学者。",
    "Java和C++的区别是什么？",
    "Python的官方教程在python.org上。",
    "机器学习常用Python库有TensorFlow和PyTorch。",
]

payload = json.dumps({
    "query": "上海天气",
    "documents": documents
})




url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/reranker/bce_reranker_base?access_token=" +token
response=requests.request("POST",url,headers=headers, data=payload.encode("utf-8"))

print(response.json())