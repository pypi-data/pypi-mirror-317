import requests
import httpx

# 定义 URL 和请求头
url = "https://www.hao6v.tv/e/search/index.php"

from urllib.parse import urlencode

# 提前对 data 进行 urlencode
data_encoded = urlencode({
    "show": "title,smalltext",
    "tempid": "1",
    "keyboard": "凡人歌".encode("gb2312"),
    "tbname": "article",
    "x": "42",
    "y": "11",
})

print(data_encoded)

headers = {
    "User-Agent": "python-requests/2.31.0",  # 确保与 requests 一致
    "Content-Type": "application/x-www-form-urlencoded",  # 明确指定表单类型
}

response = httpx.post(url, headers=headers, content=data_encoded, follow_redirects=True)
print(response.text)
