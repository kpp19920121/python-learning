import requests
from bs4 import BeautifulSoup

# 禅道的 URL 地址
bug_url = "http://10.137.25.87:8088/zentao/project-bug-658-0-0-status,id_desc-0-all-0-231-300-1.html?tid=mmwgigby"
login_url = "http://10.137.25.87:8088/zentao/user-login.html"  # 登录接口的 URL

# 禅道的用户名和密码
username = "fankea"  # 替换为实际的用户名
password = "Kpp19920121@123.com"  # 替换为实际的密码

# 创建一个会话对象，保持会话状态
session = requests.Session()

# 发送请求，获取登录页面内容（此页面通常包含 CSRF Token）
login_page = session.get(login_url)

# 使用 BeautifulSoup 解析登录页面，获取 CSRF Token（如果有的话）
soup = BeautifulSoup(login_page.text, 'html.parser')

# 解析 token（根据页面实际结构，可能是一个隐藏的输入框）
token = ""

# 准备登录的表单数据
login_data = {
    'account': username,     # 用户名
    'password': password,    # 密码
    'referer': login_url,    # 登录后重定向的 URL
    'token': token           # CSRF Token
}

# 模拟发起 AJAX 登录请求
response = session.post(login_url, data=login_data)

print(f"login_url=>{login_url}:data=>{login_data}:response=>{response}")


# 检查是否登录成功（通过检查是否重定向到首页等）
if response.url == login_url:
    print("登录失败，请检查用户名和密码")
else:
    print("登录成功！")

    # 现在可以访问受保护的页面
    bug_page = session.get(bug_url)
    soup = BeautifulSoup(bug_page.text, 'html.parser')

    # 根据页面结构提取 Bug 信息
    bug_list = []
    bug_table = soup.find('table', {'class': 'table-1'})  # 假设表格的 class 为 'table-1'

    if bug_table:
        rows = bug_table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 1:  # 跳过表头
                bug_info = {}
                try:
                    bug_info['bug_id'] = cols[0].text.strip()
                    bug_info['title'] = cols[1].text.strip()
                    bug_info['status'] = cols[2].text.strip()
                    bug_info['severity'] = cols[3].text.strip()
                    bug_info['assigned_to'] = cols[4].text.strip()
                    bug_info['created_at'] = cols[5].text.strip()
                    bug_info['updated_at'] = cols[6].text.strip()

                    bug_list.append(bug_info)
                except IndexError:
                    continue

    # 输出所有的 Bug 信息
    for bug in bug_list:
        print(f"Bug ID: {bug['bug_id']}")
        print(f"Title: {bug['title']}")
        print(f"Status: {bug['status']}")
        print(f"Severity: {bug['severity']}")
        print(f"Assigned To: {bug['assigned_to']}")
        print(f"Created At: {bug['created_at']}")
        print(f"Updated At: {bug['updated_at']}")
        print("-" * 40)
