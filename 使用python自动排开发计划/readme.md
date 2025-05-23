# 1. 项目简介 #
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;这个 Python 脚本用于根据指定的 Excel 文件，自动为开发人员排定任务的开始和结束日期，排除周末（即只计算工作日）。它会根据开发人员的上一个任务的结束日期以及工时来计算任务的开始日期和结束日期，并在原始 Excel 文件中更新相应的任务日期。最终，脚本将生成一个新的 Excel 文件，包含更新后的开始和结束日期。

# 2. 功能描述 #
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;读取 Excel 文件：加载用户指定的 Excel 文件，读取开发人员的任务数据。
计算开始和结束日期：根据开发人员的工时计算任务的开始日期和结束日期，自动排除周六和周日。
更新 Excel 文件：将计算得出的开始日期和结束日期更新到 Excel 文件中，并为修改过的单元格添加底纹标记。
生成新的 Excel 文件：生成包含更新日期的 Excel 文件，并自动调整列宽以适应内容。
# 3. 依赖 #


- Python 3.x：此脚本需要 Python 3.x 环境。


- openpyxl：用于处理 Excel 文件。


- pandas：用于处理 Excel 文件中的数据。


- datetime：用于日期处理。
可以使用以下命令安装所需的 Python 库：

		pip install -i https://pypi.tuna.tsinghua.edu.cn/simple openpyxl pandas

# 4. 使用方法 #
## 4.1. 准备工作 ##
确保您已经安装了 Python 3.x 环境。
将要处理的 Excel 文件准备好，并确保文件包含至少两个必要的列：开发人员 和 结束日期。
## 4.2. 运行脚本 ##
下载或复制脚本：下载并保存脚本到本地。

运行脚本：在命令行中，运行以下命令：

	python replace_sql_statements.py
输入 Excel 文件路径：运行脚本后，脚本会提示您输入要处理的 Excel 文件路径。例如：




- 请输入 Excel 文件路径（如未指定路径，将退出程序）：/path/to/your/excel_file.xlsx


- 输入输出文件路径：脚本会提示您输入输出文件路径。如果没有输入，默认会在原路径下生成新的文件（例如：excel_file_排好的开发计划.xlsx）。



- 输入默认开始日期：脚本会提示您输入默认开始日期。该日期将作为没有指定开始日期的开发人员任务的开始日期。




- 请输入默认开始日期（格式：YYYY-MM-DD，留空则为下一个工作日）：2024-01-01
## 4.3. 输出 ##
脚本会生成一个新的 Excel 文件，并保存至您指定的路径。
在新的 Excel 文件中，开发人员的任务开始和结束日期会被计算并更新。
脚本会自动为修改过的单元格添加底纹（红色标记已修改的行，黄色标记日期列）。
## 4.4. 示例 ##
假设您有以下 Excel 文件：

	开发人员	结束日期	   工时
	张三	    2024-01-05	     5
	李四	    2024-01-10	     3
	王五	    2024-01-07	     4
假设每个开发人员的任务持续工作日为 3 天（排除周末）。运行脚本后，假设开发人员张三、李四和王五的任务安排将被自动计算出开始和结束日期。

例如，张三的任务将在 2024-01-08（下一个工作日）开始，并在 2024-01-10 完成。

# 5. 脚本工作流程 #


- 读取 Excel 文件：加载指定路径的 Excel 文件。


- 检查列数据：确保 Excel 文件中包含必要的列 开发人员 和 结束日期。


- 计算开发人员的任务日期：
对于没有指定的开始日期，脚本将使用默认开始日期或从上一个任务结束的下一工作日开始。


- 根据任务的工时数，计算结束日期，排除周六和周日。


- 更新 Excel 文件：将计算得出的开始日期和结束日期写入 Excel 文件，并为修改过的单元格添加底纹。


- 保存并生成报告：保存更新后的 Excel 文件，并生成一个新的文件，调整列宽，确保内容显示完整。
# 6. 注意事项 #


- 备份数据：此脚本会直接修改原始 Excel 文件，因此在执行之前建议先备份原始文件。


- 日期格式：确保 Excel 文件中的日期列格式正确，脚本只会处理正确格式的日期。


- 空值处理：如果 Excel 文件中某些开发人员的结束日期为空，脚本将跳过这些行。


- 工作日计算：脚本仅会计算工作日，排除周六和周日。如果开发人员的结束日期是周五，任务将从下一个工作日（周一）开始。
# 7. 常见问题 #


- Q: 如何处理多个模块的文件？	


	- A: 如果您有多个模块的文件，可以将多个模块的文件放入同一个目录，脚本会自动处理目录下的所有 Excel 文件。



- Q: 为什么生成的 Excel 文件没有日期更新？


	- A: 请确保 Excel 文件中包含正确的列名（开发人员 和 结束日期）。如果没有匹配的列，脚本将无法更新日期。



- Q: 如何修改默认的开始日期？


	- A: 您可以在运行脚本时输入默认开始日期（格式：YYYY-MM-DD）。如果留空，脚本将自动选择下一个工作日作为默认开始日期。