from urllib import request
from bs4 import BeautifulSoup

url = "http://www.baidu.com"
with request.urlopen(url) as f:
    html = f.read().decode("utf-8")
    soup = BeautifulSoup(html, features = "html.parser")
    arr = soup.find_all("img")
    for string in arr:
        print(string)
