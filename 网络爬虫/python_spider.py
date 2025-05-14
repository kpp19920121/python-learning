import requests
from bs4 import BeautifulSoup, Tag

response=requests.request(url="https://www.zhcw.com/kjxx/ssq/",method="GET")


print(f"response.status_code=->{response.status_code}")

if response.status_code==200:
    soup = BeautifulSoup(response.text, 'html.parser')



    tag_list=[temp.name for temp in soup.findAll(True)]

    for temp in tag_list:
        print(temp)