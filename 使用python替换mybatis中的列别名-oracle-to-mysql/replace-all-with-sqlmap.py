import os
import re

def convert_columns_to_uppercase(sql):
    """
    将 SQL 语句中的列名和别名转换为大写，保留 SELECT, FROM 等关键字不变。
    """
    # 匹配 SELECT 和 FROM 之间的内容，并只对其中的列名进行转换
    # 匹配列名和别名，确保只有字段名被转换为大写
    def replace_column_name(match):
        column = match.group(1)  # 获取列名或别名
        return column.upper()    # 将列名转为大写

    # 正则表达式匹配 SELECT 和 FROM 之间的部分的列名
    sql = re.sub(
        r'(?<=\bselect\b)([\s\S]*?)(?=\bfrom\b)',  # 匹配列名或别名
        replace_column_name,        # 执行替换
        sql,
        flags=re.IGNORECASE         # 忽略大小写
    )

    return sql

def process_mapper_file(file_path):
    """
    处理 MyBatis 的 mapper 文件，提取并替换 SELECT 语句中的列名和别名。
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配 <select> 标签中的 SQL 语句
        def replace_sql_in_select_tag(match):
            # 获取 <select> 标签中的属性部分
            select_tag_start = match.group(1)  # <select ...>
            # 获取 <select> 标签中的 SQL 内容
            original_sql = match.group(2)  # SELECT SQL 内容
            print(f"处理前sql:\n{original_sql}")
            # 将 SELECT 和 FROM 之间的列名转换为大写
            modified_sql = convert_columns_to_uppercase(original_sql)
            print(f"处理后sql:\n{modified_sql}")
            # 返回替换后的 <select> 标签内容，保留原有的属性
            return f"{select_tag_start}{modified_sql}</select>"

        # 改进正则表达式，确保只匹配到 <select> 标签的内容
        modified_content = re.sub(
            r'(<select(?!Key)[^>]*>)([\s\S]*?)(</select>)',  # 匹配 <select> 标签的内容
            replace_sql_in_select_tag,
            content
        )

        # 写回文件
        with open(file_path, 'w', encoding='utf-8',newline='') as f:
            f.write(modified_content)

        print(f"已处理文件：{file_path}")

    except Exception as e:
        print(f"处理文件时出错：{file_path}，错误：{e}")

def process_directory(directory):
    """
    遍历指定目录，处理所有 MyBatis Mapper 文件。
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.xml'):  # 仅处理 .xml 文件
                process_mapper_file(os.path.join(root, file))

if __name__ == "__main__":
    # 输入需要处理的 MyBatis Mapper 文件目录
    directory = input("请输入 MyBatis Mapper 文件所在目录路径：").strip()
    if os.path.isdir(directory):
        process_directory(directory)
    else:
        print("输入的目录无效，请检查路径。")
