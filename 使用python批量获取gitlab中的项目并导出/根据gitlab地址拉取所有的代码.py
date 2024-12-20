import os
import subprocess
import gitlab
import requests
from concurrent.futures import ThreadPoolExecutor

# 设置 base_url 和 Personal Access Token
#gitlab的url
base_url = "https://192.168.233.133:30443"

#gitlab中配置的token
token = "-KJgwpw9UCNaXHT2G-xx"  # 替换为你生成的 Token


#群组信息
subGroup="xxx/xxx/xxx/xxx"


# 获取当前脚本所在目录路径
script_dir = os.path.dirname(os.path.realpath(__file__))

# 设置目标目录为脚本所在目录下的一个子目录
target_dir = script_dir

# 创建目标目录（如果不存在）
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 连接到 GitLab 实例
gl = gitlab.Gitlab(base_url, private_token=token, ssl_verify=False)

# 打印 base_url
print(f"base_url => {base_url}")

# 获取所有群组，通过 API 获取群组信息
def get_groups(parentId=None):
    url = f"{base_url}/api/v4/groups"


    if parentId is None or parentId=='None':
        print("没有传入 parentId，使用默认操作")
        # 如果没有传值，可以执行默认的逻辑（例如获取所有群组）
        url = f"{base_url}/api/v4/groups"
    else:
        print(f"传入的 parentId 为: {parentId}")
        # 如果传入了 parentId，可以根据该 ID 获取特定群组
        url = f"{base_url}/api/v4/groups/{parentId}"

    print(f"b获取所有的用户组的地址为:{url}")

    headers = {"PRIVATE-TOKEN": token}
    try:
        response = requests.get(url, headers=headers, verify=False)  # 禁用 SSL 校验
        response.raise_for_status()  # 检查请求是否成功
        return response.json()  # 返回 JSON 数据
    except requests.exceptions.RequestException as e:
        print(f"请求错误: {e}")
        return []

# 处理 API 返回的数据
groups_data = get_groups()

# 提取目标群组信息，查找 'efpg' 和 'newzhonglv'
# 提取目标群组信息，查找包含或完全匹配的子群组路径
def extract_group_info(groups_data, subGroup):
    parent_group = None

    for group in groups_data:
        # 如果 full_path 包含 subGroup
        if subGroup == group['full_path']:
            parent_group = group
            print(f"父群组 '{subGroup}' 在 full_path 中，ID: {group['id']}, URL: {group['web_url']}")
        # 如果 full_path 完全等于 subGroup
        elif subGroup in group['full_path']:
            parent_group = group
            print(f"父群组 '{subGroup}' 完全匹配，ID: {group['id']}, URL: {group['web_url']}")
            groups_data = get_groups(f"{group['parent_id']}")
            parent_group=groups_data

    return parent_group

# 假设我们要查找 'efpg/newzhonglv' 这个子群组

parent_group = extract_group_info(groups_data, subGroup)



# 获取目标子群组下的项目
def get_projects_from_subgroup(parent_group):
    projects = []
    if parent_group:
        url = f"{base_url}/api/v4/groups/{parent_group['id']}/projects?per_page=100"
        print(f"获取群组下的所有项目 URL 为: {url}")
        headers = {"PRIVATE-TOKEN": token}
        try:
            response = requests.get(url, headers=headers, verify=False)  # 禁用 SSL 校验
            response.raise_for_status()  # 检查请求是否成功
            projects = response.json()  # 返回项目列表
        except requests.exceptions.RequestException as e:
            print(f"请求错误: {e}")
    return projects

# 获取子群组的所有项目
projects = get_projects_from_subgroup(parent_group)

# 克隆或更新仓库的函数
def clone_or_pull_repo(project):
    repo_url = f"{base_url}/{project['namespace']['full_path']}/{project['name']}.git"  # 获取仓库的 HTTP 克隆 URL
    repo_name = project['name']  # 获取仓库名
    repo_target_path = os.path.join(target_dir, repo_name)

    if os.path.exists(repo_target_path):
        print(f"仓库 {repo_name} 已经存在，执行 git pull...")
        # 进入仓库目录，执行 git pull 命令
        try:
            subprocess.run(['git', '-C', repo_target_path, 'pull'], check=True)
            print(f"仓库 {repo_name} 更新成功！")
        except subprocess.CalledProcessError as e:
            print(f"更新仓库 {repo_name} 失败: {e}")
    else:
        print(f"仓库 {repo_name} 不存在，执行 git clone...")
        # 克隆仓库
        try:
            subprocess.run(['git', 'clone', repo_url, repo_target_path], check=True)
            print(f"仓库 {repo_name} 克隆成功！")
        except subprocess.CalledProcessError as e:
            print(f"克隆仓库 {repo_name} 失败: {e}")

# 使用 ThreadPoolExecutor 进行并行克隆或更新
with ThreadPoolExecutor() as executor:
    executor.map(clone_or_pull_repo, projects)

print("所有仓库克隆或更新完成。")
