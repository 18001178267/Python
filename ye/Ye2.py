import requests  # 发送http请求
from bs4 import BeautifulSoup  # 解析html
import lxml  # 解析器 中文不乱码
import os  # 创建文件夹
import ssl

import urllib.request
import re

url = 'https://www.948mk.com/move/2/'

j=1

for i in range(1,2):
    request = urllib.request.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
    response = urllib.request.urlopen(request)
    buf = response.read()
    buf = str(buf, encoding='UTF-8',errors='ignore')
    #print(buf)
    # 获取所有图片url地址列表
    listurl = re.findall(r'http.+\.jpg', buf)
    #with open(r'C:\Users\YZW\Desktop\py\1.txt', 'w') as f:
    #    f.write(str(listurl)+'\n')
    print(listurl)
    for a in listurl:
        f = open('C:\\Users\\YZW\\Desktop\\py\\ye\\'+str(j)+'.jpg', 'wb+')
        a = urllib.request.Request(a)
        a.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36')
        try:
            req = urllib.request.urlopen(a,timeout=5)
            buf2 = req.read()
            # buf = str(buf)
            f.write(buf2)
        except:
            pass
        j += 1
