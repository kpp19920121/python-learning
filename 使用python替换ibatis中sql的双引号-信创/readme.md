# 介绍 #
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这个脚本用于处理指定目录下的 XML 文件，查找 `<select>` 语句并将其中的 resultType="java.util.Map" 替换为 resultMap，同时为每个匹配的 `<select>` 语句生成一个对应的 ResultMap 内容，并将修改后的文件保存。最终，脚本会生成一个 HTML 格式的报告，列出每个文件中修改过的 selectId 以及对应的 ResultMap 内容。

# 功能 #

- 查找 `<select>` 语句：扫描指定目录下的所有 XML 文件，查找符合特定条件的 `<select>` 语句（resultType="java.util.Map"）。


- 生成 ResultMap：为每个匹配的 `<select>` 语句生成一个对应的 ResultMap，并将列名转换为大写，别名保持不变。


- 替换 select 语句中的 resultType：将 resultType="java.util.Map" 替换为 resultMap="resultMapId"，其中 resultMapId 是根据 selectId 生成的。

- 生成后的文件会替换源文件，请谨慎操作，需要做对应的测试。

- 生成 HTML 报告：生成一份 HTML 格式的报告，列出修改过的文件路径、selectId 以及对应的 ResultMap 内容。


- 自动打开报告：在报告生成后，自动在默认浏览器中打开报告。
# 依赖 #


- Python 3.x


- webbrowser 模块（Python 标准库）


- re 模块（Python 标准库）


- os 模块（Python 标准库）
# 使用方法 #


1. 下载脚本
将脚本下载到本地并解压到一个文件夹中。



2. 运行脚本
打开终端或命令行，进入脚本所在目录。
运行脚本：

		python replace_sql_statements.py
注：确保 Python 3 已经安装，并且在系统的 PATH 中。

3. 输入目录路径
运行脚本后，脚本会提示你输入要处理的文件夹路径。输入路径并按回车键。

4. 确认操作
脚本会显示你输入的文件夹路径，并询问是否继续操作：
确认要继续处理这个路径吗, 需要替换源文件？(yes/no):
输入 yes 继续处理，输入 no 取消操作。
5. 处理文件
如果确认操作，脚本将会遍历指定目录及其子目录，查找所有 .xml 文件，并处理其中的 `<select>` 语句。修改后的文件会保存为原文件名，并以 .xml 后缀保存。

6. 查看报告
脚本会生成一个 HTML 格式的报告，展示修改的详细信息。报告会保存在当前工作目录下，并会自动在浏览器中打开。

# 脚本工作流程 #


- 读取 XML 文件：读取指定路径下的每个 .xml 文件。


- 查找并处理 `<select>` 语句：


	- 使用正则表达式查找符合 resultType="java.util.Map" 的 `<select>` 语句。


	- 对于每个符合条件的 `<select>` 语句，生成一个 ResultMap。


	- 将 select 语句中的 resultType 替换为对应的 resultMap。


- 生成 ResultMap：
根据列名生成 ResultMap，列名转换为大写，别名保持原样。


- 保存修改后的文件：将修改后的内容写入新的 XML 文件。


- 生成 HTML 报告：生成一个 HTML 格式的报告，列出文件路径、selectId 以及对应的 ResultMap 内容。


- 自动打开报告：脚本完成后会自动在默认浏览器中打开报告。
# 示例 #
假设你有以下 XML 文件：


		<mapper namespace="com.example.dao">
		    <select id="selectUser" resultType="java.util.Map" parameterType="java.util.Map">
		        select id, username as "userName" from users
		    </select>
		</mapper>

运行脚本后，select 语句会被替换为：

	<mapper namespace="com.example.dao">
	    <select id="selectUser" resultMap="selectUserResultMap" parameterType="java.util.Map">
	        select id, username as "userName" from users
	    </select>
	    <resultMap id="selectUserResultMap" type="java.util.Map">
	        <result column="ID" property="userName" javaType="java.lang.String"></result>
	    </resultMap>
	</mapper>

同时，生成的 HTML 报告会列出所有替换的信息。

# 注意事项 #


- 请确保所提供的目录路径是正确的，并且包含 .xml 文件。


- 脚本会直接修改文件并覆盖原文件，建议在运行前备份原始文件。


- 只会替换 resultType="java.util.Map" 的 `<select>` 语句，如果 XML 文件中的 select 语句没有该属性，脚本不会做任何修改。


- 如果文件较大，或目录包含大量文件，可能需要一些时间来处理。
# 常见问题 #


- Q: 如何处理多个模块的文件？


- A: 如果你有多个模块的文件，只需要分别运行脚本，或者将多个模块的文件放入同一个目录中，脚本会遍历该目录下的所有 XML 文件进行处理。



- Q: 为什么生成的报告没有显示任何内容？


- A: 请检查 XML 文件中是否包含符合条件的 `<select>` 语句（即 resultType="java.util.Map"）。如果没有符合条件的语句，报告会为空。

