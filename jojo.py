from urllib import request
from bs4 import BeautifulSoup
import threading
import os

downloadUrl = "http://www.manhuadb.com"
urlMap = {
    1: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13260_p",
        "size": 202
    },
    2: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13255_p",
        "size": 196
    },
    3: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13264_p",
        "size": 210
    },
    4: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13261_p",
        "size": 192
    },
    5: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13263_p",
        "size": 194
    },
    6: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13253_p",
        "size": 194
    },
    7: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13252_p",
        "size": 192
    },
    8: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13258_p",
        "size": 196
    },
    9: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13256_p",
        "size": 188
    },
    10: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13257_p",
        "size": 190
    },
    11: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13265_p",
        "size": 190
    },
    12: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13262_p",
        "size": 194
    },
    13: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13250_p",
        "size": 192
    },
    14: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13266_p",
        "size": 188
    },
    15: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13259_p",
        "size": 188
    },
    16: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13251_p",
        "size": 232
    },
    17: {
        "baseUrl": "http://www.manhuadb.com/manhua/139/1328_13254_p",
        "size": 264
    }
}

def downloadOnePage(_vol, _page, _url):
    fileName = "output/jojo6/" + str(_vol) + "/" + str(_page) + ".jpg"
    if not os.path.exists(fileName):
        try:
            print("第" + str(_vol) + "话第" + str(_page) + "页开始下载...")
            with request.urlopen(_url, timeout=30) as f:
                html = f.read().decode("utf-8")
                soup = BeautifulSoup(html, features="html.parser")
                src = downloadUrl + soup.find("img", "img-fluid")['src']
                request.urlretrieve(src, fileName)
                print("第" + str(_vol) + "话第" + str(_page) + "页下载完成！")
        except:
            print("第" + str(_vol) + "话第" + str(_page) + "页发生异常！！！")
            downloadOnePage(_vol, _page, _url) # 再次调用

vol = 1
while vol <= 17:
    page = 1
    while page <= urlMap[vol]["size"]:
        url = urlMap[vol]["baseUrl"]
        if page != 1:
            url += str(page)
        url += ".html"
        threading.Thread(target=downloadOnePage, args=[vol, page, url]).start()
        page += 1
    vol += 1
