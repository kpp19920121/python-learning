import os
import subprocess
import shutil
from concurrent.futures import ThreadPoolExecutor

# 定义要扫描的根目录

# 用户输入 Excel 文件路径
root_directory = input("请输入打包文件源码路径()：").strip()
if not root_directory or not os.path.exists(root_directory):
    raise FileNotFoundError(f"文件路径无效或不存在：{root_directory}")

# 获取指定目录下的第一级子目录
def get_directories(root_directory):
    try:
        # 仅获取第一级子目录
        subdirs = [os.path.join(root_directory, d) for d in os.listdir(root_directory)
                   if os.path.isdir(os.path.join(root_directory, d))]
        return subdirs
    except Exception as e:
        print(f"Error reading directories: {e}")
        return []

# 检查目录中是否存在 pom.xml 文件
def has_pom_file(directory):
    pom_file = os.path.join(directory, 'pom.xml')
    return os.path.exists(pom_file)

# 执行 Maven 打包命令
def build_project(project_directory, dist_directory):
    print(f"Building project in {project_directory}")
    mvn_command = f"mvn clean install -Dmaven.test.skip=true -f {project_directory}/pom.xml"
    try:
        subprocess.check_call(mvn_command, shell=True)
        print(f"Build successful for {project_directory}")

        new_war_file_name=""

        # 查找生成的 war 包文件
        war_file = None
        for root, dirs, files in os.walk(project_directory):
            for file in files:
                if "-service" in file and  (file.endswith(".jar") or file.endswith(".war")):
                    print(f"开始拷贝war包并判断war包名称是否需要重命名{file}")
                    war_file = os.path.join(root, file)

                    if "-4.1.2" in file:
                        base_name, ext = os.path.splitext(file)
                        new_war_file_name=file.split('-4.1.2')[0]+ext
                        print(f"重命名后的war包名称为:{war_file}")
                    else:
                        new_war_file_name=file
            if war_file:
                break
        print(f"war_file=>:{war_file}:dist_directory=>{dist_directory}")
        if war_file:
            print("开始拷贝war包")
            # 拷贝 WAR 文件到指定目录
            if not os.path.exists(dist_directory):
                os.makedirs(dist_directory)
            shutil.copy(war_file, dist_directory+"/"+new_war_file_name)
            print(f"Copied {war_file} to {dist_directory}")
        else:
            print(f"No WAR file found in {project_directory}")

    except subprocess.CalledProcessError as e:
        print(f"Build failed for {project_directory}: {e}")

# 主程序
def main():
    # 获取用户指定的输出目录，若未输入则使用默认的 dist 目录
    dist_directory = input("Enter the output directory for WAR files (default: './dist'): ").strip()
    if not dist_directory:
        dist_directory = os.path.join(root_directory, "dist")

    project_dirs = get_directories(root_directory)

    # 设置并行的最大线程数，避免过多线程导致系统负载过高
    max_threads = 4
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # 提交任务并行执行
        for project_dir in project_dirs:
            if has_pom_file(project_dir):
                executor.submit(build_project, project_dir, dist_directory)

if __name__ == "__main__":
    main()
