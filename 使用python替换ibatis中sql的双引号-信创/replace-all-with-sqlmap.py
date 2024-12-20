import os
import re
import webbrowser  # 导入 webbrowser 模块，用于自动打开 HTML 报告

# 替换 select 语句中的 resultType 为 resultMap，并生成相应的 ResultMap 内容
def replace_select_statements(file_path):
    """
    该函数读取指定的 XML 文件，查找符合条件的 select 语句，
    将其中的 resultType 属性替换为 resultMap，生成相应的 ResultMap 内容，
    并将修改后的文件保存。返回包含替换信息的列表。
    """
    # 动态获取模块名称，可以根据实际需要进行调整
    module_name = "ifinance-xxx-service"  # 模块名称，用于生成报告时的标题

    # 读取指定路径的 XML 文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()  # 读取整个 XML 文件的内容

    # 使用正则表达式匹配符合条件的 <select> 标签，提取 selectId、selectColumns 和 tableName
    select_pattern = re.compile(
        r'<select\s+id="([^"]+)"\s+resultType="java\.util\.Map"\s+parameterType="java\.util\.Map">\s*'
        r'select\s+(.*?)\s+from\s+(.*?)(\s*<\s*/\s*select>)',
        re.DOTALL | re.IGNORECASE  # DOTALL 允许跨多行匹配，IGNORECASE 使正则不区分大小写
    )

    # 查找所有匹配的 <select> 语句
    matches = select_pattern.findall(content)
    result_maps = []  # 用于存储替换后的结果，包括文件路径、selectId 和 ResultMap 内容

    # 如果没有找到匹配的 select 语句，则输出提示信息并返回空字符串
    if not matches:
        print(f"路径下 {file_path} 未搜索到匹配的 SQL, 直接返回")
        return ""

    # 遍历每个匹配的 select 语句，进行替换
    for match in matches:
        select_id = match[0]  # 提取 select 语句的 id
        select_columns = match[1]  # 提取 select 语句中的列部分
        table_name = match[2]  # 提取 select 语句中的表名（虽然后续未使用）

        # 打印匹配到的内容，便于调试
        print(f"匹配到文件: {match[0]} - {match[1]} - {match[2]}")

        # 使用正则表达式匹配 select 语句中的列名和列别名，处理 'AS' 和不带 'AS' 的情况
        column_pattern = re.compile(r'(\w+)\s+(?:as\s+)?+"([^"]+)"', re.IGNORECASE)
        columns = column_pattern.findall(select_columns)  # 提取列名和别名

        # 为当前的 select 语句生成对应的 ResultMap 内容
        result_map_id = f"{select_id}ResultMap"  # 为每个 select 语句生成一个独立的 ResultMap ID
        result_map_entries = []  # 用于存储每一列的 <result> 标签内容

        # 遍历每一列，生成相应的 <result> 标签，将列名转换为大写，别名保持不变
        for column, alias in columns:
            result_map_entries.append(f'\t\t<result column="{column.upper()}" property="{alias}" javaType="java.lang.String"></result>')

        # 将所有的 <result> 标签拼接成一个完整的 ResultMap 内容
        result_map_content = (
                f'\t<resultMap id="{result_map_id}" type="java.util.Map">\n'
                + "\n".join(result_map_entries) + "\n"
                + '\t</resultMap>'  # 结束 <resultMap> 标签
        )

        # 替换 select 语句中的 resultType 为新的 resultMap ID
        content = content.replace(
            f'<select id="{select_id}" resultType="java.util.Map" parameterType="java.util.Map">',
            f'<select id="{select_id}" resultMap="{result_map_id}" parameterType="java.util.Map">'
        )

        # 找到 <mapper> 标签并将生成的 ResultMap 内容添加到其下
        mapper_pattern = re.compile(r'(<mapper[^>]*>)', re.IGNORECASE)
        content = mapper_pattern.sub(r'\1\n' + result_map_content, content)

        # 将替换后的信息添加到结果列表
        result_maps.append((file_path, select_id, result_map_content))  # 将文件路径、selectId 和 ResultMap 内容添加到列表中

    # 将修改后的内容写入到新的 XML 文件中
    # 输出文件路径为原路径，但后缀改为 .xml
    output_file_path = os.path.splitext(file_path)[0] + ".xml"

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(content)  # 将修改后的 XML 内容写入文件

    return result_maps  # 返回包含文件路径、selectId 和 ResultMap 内容的列表


# 生成 HTML 格式的报告
def generate_html_report(result_maps, module_name):
    """
    该函数根据传入的 result_maps 生成一个 HTML 格式的报告，报告展示了文件路径、selectId 以及对应的 ResultMap。
    并将报告保存为 .html 文件，最后自动在浏览器中打开。
    """
    # 创建 HTML 文件的基本结构
    html_content = f'''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{module_name} 结果报告</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>{module_name} 结果报告</h1>
        <table>
            <tr>
                <th>模块名称</th>
                <th>文件路径</th>
                <th>替换的 selectId</th>
                <th>对应的 ResultMap</th>
            </tr>
    '''

    # 按文件路径分组结果
    report_data = {}  # 创建字典，用于根据文件路径分组 ResultMap
    for file_path, select_id, result_map in result_maps:
        if file_path not in report_data:
            report_data[file_path] = []  # 如果该文件路径不存在，则创建一个空列表
        report_data[file_path].append((select_id, result_map))  # 将每个 selectId 和 ResultMap 添加到对应的文件路径下

    # 生成每个文件的结果报告
    for file_path, selects in report_data.items():
        select_ids = ', '.join(select[0] for select in selects)  # 获取所有 selectId
        result_maps_combined = '<br>'.join(select[1] for select in selects)  # 合并所有 ResultMap，以换行分隔

        html_content += f'''
            <tr>
                <td>{module_name}</td>
                <td>{file_path}</td>
                <td>{select_ids}</td>
                <td><pre>{result_maps_combined}</pre></td>  <!-- 显示所有 ResultMap -->
            </tr>
        '''

    html_content += '''
        </table>
    </body>
    </html>
    '''

    # 将 HTML 内容写入文件
    output_file_path = os.path.join(os.getcwd(), f"{module_name}.html")
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(html_content)  # 将 HTML 内容写入文件

    # 自动打开生成的 HTML 报告
    webbrowser.open(f'file:///{output_file_path}')  # 使用默认浏览器打开报告


# 处理指定目录下的所有 XML 文件
def process_directory(directory_path):
    """
    该函数遍历指定目录下的所有 XML 文件，调用 replace_select_statements 函数处理每个文件，
    然后生成最终的 HTML 报告。
    """
    print(f"开始搜索路径下匹配的 SQL 语句 {directory_path}")

    # 检查目录路径是否存在
    if not os.path.exists(directory_path):
        print(f"错误：目录 '{directory_path}' 不存在。")
        return

    result_maps = []  # 存储所有替换后的结果

    # 遍历目录下所有文件，并筛选出 .xml 文件
    for root, _, files in os.walk(directory_path):
        for filename in files:
            if filename.endswith(".xml"):  # 处理以 .xml 结尾的文件
                file_path = os.path.join(root, filename)  # 获取文件的完整路径
                result_maps.extend(replace_select_statements(file_path))  # 调用替换函数并累积结果

    # 生成 HTML 报告
    generate_html_report(result_maps, "ifinance-xxx-service")


# 主程序入口
if __name__ == "__main__":
    # 获取用户输入的目录路径并确认操作
    directory_path = input("请输入要处理的文件夹路径: ").strip()

    print(f"您即将处理以下目录：{directory_path}")
    confirmation = input("确认要继续处理这个路径吗, 需要替换源文件？(yes/no): ").strip().lower()

    if confirmation == 'yes':
        print("操作即将开始。")
        process_directory(directory_path)  # 开始处理目录
    else:
        print("操作已取消。")
