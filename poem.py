import re
from xpinyin import Pinyin
p = Pinyin()

with open("./poem_input.txt", "r") as f:
    raws = f.read()
raws = re.sub('“|”', "", raws)
poems = re.split('\s|\n+|，|。|！|？|；|：', raws)
# 去除空格
poems = [poem for poem in poems if poem != '']

result = {}
for poem in poems:
    firstPinyin = p.get_pinyin(poem[0])
    if firstPinyin in result:
        result[firstPinyin].append(poem)
    else:
        result[firstPinyin] = [poem]

sortedKeys = sorted(result.keys())

#写入文件
with open("./output/poem_output.txt", "w") as f:
    for key in sortedKeys:
        f.write(key + "\n")
        for poem in result[key]:
            f.write(poem + "\n")
        f.write("\n")

print("输出完成")
