import requests  # 发送http请求
from bs4 import BeautifulSoup  # 解析html
import lxml  # 解析器 中文不乱码
import os  # 创建文件夹
import pandas #处理csv，Excel
import urllib.request
import re
 
url = 'https://movie.douban.com/top250'
request = urllib.request.Request(url)
request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
response = urllib.request.urlopen(request)
buf = response.read()
#print(type(buf))  #byte类型
buf = str(buf, encoding='utf-8',errors='ignore')
# print(buf)
# 获取所有图片url地址列表
listurl = re.findall(r'http.+\.jpg', buf)
with open(r'C:\Users\YFZX\Desktop\py\1.txt', 'w') as f:
    f.write(str(listurl)+'\n')
print(listurl,'\n')
 
i = 1
for a in listurl:
    f = open(str(i)+'.jpg', 'wb+')
    req = urllib.request.urlopen(a)
    buf = req.read()
    print(buf)
    # buf = str(buf)
    f.write(buf)
    i += 1