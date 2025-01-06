import re

# SQL语句的模式
sql_pattern = re.compile(r'''
    \bSELECT\b        # 匹配 SELECT 关键字
    \s+.*?\bFROM\b    # 匹配 FROM 关键字及其前面的内容
    \s+.*?\bWHERE\b   # 匹配 WHERE 关键字及其前面的内容
    \s+.*             # 匹配 WHERE 子句及其后面的内容，包括可能的字符串拼接
    ''', re.IGNORECASE | re.DOTALL | re.VERBOSE)

# 测试用例
test_sql = """
SELECT *
FROM users
WHERE user_id = 1
  AND username = 'admin'
"""


# 匹配测试
matches = re.findall(sql_pattern, strSQL)
if matches:
    print("匹配到的SQL语句：")
    for match in matches:
        print(match.strip())
else:
    print("未找到匹配的SQL语句。")