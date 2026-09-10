import requests

# 访问百度首页
response = requests.get("https://www.baidu.com")

# 打印返回的 HTML 内容（前500个字符）
print(response.text[:5000])

list = [1,2,3,]
print(list)
print()
list = [2,3]
print
