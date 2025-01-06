# MyBatis Mapper 文件列名转换脚本 #
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这个脚本用于处理 MyBatis Mapper 文件中的 SQL 语句，特别是 `<select>` 标签内的 SQL 内容。它会将 SELECT 和 FROM 之间的列名和别名转换为大写字母。该脚本会遍历指定目录下的所有 .xml 文件，找到所有的 `<select>` 标签并替换其中的列名。

# 功能说明 #


- 列名转换：只转换 SQL 语句中 SELECT 和 FROM 之间的列名和别名为大写，保留 SQL 关键字如 SELECT、FROM、WHERE 等的大小写不变。


- 处理 `<select>` 标签：脚本会读取文件中的所有 `<select>` 标签，提取并处理其中的 SQL 语句。


- 目录处理：可以指定一个目录，脚本会自动遍历目录中的所有 .xml 文件，处理其中的 `<select>` 标签。
# 使用方法 #
1. 克隆或下载脚本
下载此脚本文件，并确保 Python 环境已经安装。

2. 安装依赖
该脚本使用 Python 标准库中的模块，不需要额外安装第三方依赖。

3. 运行脚本
在命令行中运行脚本。输入以下命令启动脚本：

		python process_mapper_files.py

4. 输入目录路径
运行脚本后，系统会提示你输入 MyBatis Mapper 文件所在的目录路径。输入路径后，脚本将遍历该目录及其子目录，处理所有 .xml 文件。

		请输入 MyBatis Mapper 文件所在目录路径：/path/to/your/mapper/files

5. 文件处理
脚本会遍历目录中的所有 .xml 文件，对于每个文件，脚本会提取并修改 `<select>` 标签中的 SQL 语句，将 SELECT 和 FROM 之间的列名转换为大写。

6. 修改结果
处理完成后，脚本会将修改后的内容写回原文件。你可以在文件中查看处理结果，确保 SQL 列名已经正确转换为大写。

7. 错误处理
如果在处理文件时发生任何错误，脚本会打印出错误信息，包括无法访问的文件或路径、正则匹配问题等。

示例
假设你有一个如下的 XML 文件：


	<select id="getUser" resultType="User">
	    select id, name, email from users where status = 1
	</select>

运行脚本后，文件中的 SQL 会被修改为：


	<select id="getUser" resultType="User">
	    SELECT ID, NAME, EMAIL FROM USERS WHERE STATUS = 1
	</select>

# 代码说明 #
1. convert_columns_to_uppercase(sql)
该函数接受一个 SQL 语句，将 SELECT 和 FROM 之间的列名和别名转换为大写。



	- 使用正则表达式 (?<=\bselect\b)([\s\S]*?)(?=\bfrom\b) 匹配 SELECT 和 FROM 之间的内容，并调用 replace_column_name 函数将列名转换为大写。
2. process_mapper_file(file_path)
该函数处理给定的 MyBatis Mapper 文件，提取并替换文件中所有 `<select>` 标签中的 SQL。



	- 通过正则表达式 (<select(?!Key)[^>]*>)([\s\S]*?)(</select>) 匹配 `<select>` 标签的内容。


	- 对于匹配到的 SQL 内容，调用 convert_columns_to_uppercase 函数进行列名转换。


	- 修改后的内容会写回原文件。
3. process_directory(directory)
该函数遍历指定目录下的所有 .xml 文件，调用 process_mapper_file 处理每个文件。

4. 主函数
if __name__ == "__main__": 部分会让脚本从命令行启动，要求用户输入文件目录路径，并开始处理文件。

# 注意事项 #


- 脚本假定文件的编码为 utf-8，确保你的文件编码为 utf-8。


- 脚本会覆盖原文件，确保在运行之前备份文件。


- 脚本只处理 `<select>` 标签中的 SQL 内容，其他 SQL 语句不会被处理。


- 如果目录中有不需要处理的文件，可以手动排除。
# 错误处理 #
如果脚本无法访问指定路径或文件，它将输出相应的错误信息并停止执行。常见错误包括：



- 目录路径错误


- 文件权限不足


- 正则匹配失败
