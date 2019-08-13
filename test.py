import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from urllib import request, parse
import re
import prettytable as pt

def parseOneFloor (floor):
    p = re.compile('<a rel="noreferrer" href="(.*?)".*?class="j_th_tit ">(.*?)</a>.*?<a.*? class=".*?frs-author-name.*?".*?>(.*?)</a>', re.S)
    r = re.search(p, floor)
    obj = {
        "title": r.group(2),
        "author": r.group(3),
        "url": "http://tieba.baidu.com" + r.group(1)
    }
    for key in obj:
        obj[key] = removeImg(obj[key])
    return obj

def removeImg (string):
    p = re.compile('<img.*?>')
    return re.sub(p, "", string)

# for page in range(547):
#     url = "http://tieba.baidu.com/f?kw=%E4%B8%BD%E6%B0%B4%E4%B8%AD%E5%AD%A6&ie=utf-8&pn=" + str(page * 50)
#     with request.urlopen(url) as f:
#         res = f.read().decode("utf-8")
#         pattern = re.compile('<li class=" j_thread_list.*?".*?>(.*?)</li>', re.S)
#         result = re.findall(pattern, res)
#         if result:
#             for i in range(len(result)):
#                 o = parseOneFloor(result[i])
#                 if o["author"] == "小扣JB":
#                     print(page + 1, o["title"], o["author"], o["url"])

def parsePoem (poemUrl):
    with request.urlopen(poemUrl) as pf:
        html = pf.read().decode("utf-8")
        poemP = re.compile('<div class="contson" id="contson[0-9a-z]{12}">(.*?)</div>', re.S)
        poem = re.search(poemP, html).group(1)
        poem = re.sub('</?p.*?>', "", poem)
        poem = re.sub('[(（‘「『【].*?[)）’」』】]', "", poem)
        poem = re.sub('<br.*?>', "", poem)
        poem = re.sub('&nbsp;', "", poem)
        poem = re.sub('<strong>[上中下]篇</strong>', "", poem)
        poem = re.sub('\s', "", poem)
        return poem.strip()

mainUrl = "https://so.gushiwen.org/wenyan/gaowen.aspx"
with request.urlopen(mainUrl) as f:
    mainHtml = f.read().decode("utf-8")
    mainP = re.compile('<span><a href="(/shiwenv_[0-9a-z]{12}\.aspx)" target="_blank">.*?</a>.*?</span>', re.S)
    uriArr = re.findall(mainP, mainHtml)
    parsePoem("https://so.gushiwen.org/shiwenv_508647475cf8.aspx")
    with open("./output/testPoem.txt", "w") as f2:
        for uri in uriArr:
            url = "https://so.gushiwen.org" + uri
            poem = parsePoem(url)
            try:
                f2.write(poem + "\n")
            except UnicodeEncodeError:
                pass

