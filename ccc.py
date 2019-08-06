from urllib import request
import re

nameArr = []
# 逐行读取
for line in open("./input.txt"):
    nameArr.append(line.strip())
# 过滤空行
nameArr = [name for name in nameArr if name != '']

for name in nameArr:
    # 小写，空格转杠
    lowerName = name.lower().replace(' ', '-')
    url = "http://www.uipmworld.org/athlete/" + lowerName
    result = name
    # 打开url
    try:
        with request.urlopen(url) as f:
            # 获取http response
            res = f.read().decode("utf-8")
            # 找到了，正则匹配
            if 'class="ranking-0 ranking"' in res:
                p = re.compile('<div class="ranking-0 ranking">.*?<div class="title">(.*?)</div>.*?<div class="rank">.*?<div class="value">(.*?)</div>.*?</div>.*?</div>', re.S)
                r = re.search(p, res)
                # r.group(n)对应正则里第n个括号匹配到的内容 这里1是标题 2是名次
                result = result + " " + r.group(1) + " " + r.group(2)
            # 没找到
            else:
                result = result + " could not be found"
    # 捕获http异常，如404，则未找到
    except Exception:
        result = result + " could not be found"
    #输出结果
    print(result)