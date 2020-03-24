import requests  # 发送http请求
from bs4 import BeautifulSoup  # 解析html
import lxml  # 解析器 中文不乱码
import os  # 创建文件夹
import ssl

import urllib.request
import re

import matplotlib.pyplot as plt
import numpy as np
import time
from math import *




plt.ion() #开启interactive mode 成功的关键函数
plt.figure()
t = []
t_now = 0
m = []
a=1
while(a):
    plt.clf() #清空画布上的所有内容
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    buf=requests.get(url = 'http://115.29.209.155:8080/TFSV1_sensor/vehicle.ak?method=get_sensor_data&imei=866262042535996&endTime=2019-10-22%2014:42:18',headers=headers)
    #buf是response类型，不是str类型；buf.text才是str类型
    #a=isinstance(buf, str)
    #print(a)
    buf=buf.text[14:21]
    print(buf)
    buf = re.findall(r'\d+.?\d*', buf) # 返回一个list类型数据
    buf=str(buf[0])
    data=float(buf)
    #print(data)
    t_now = data
    t.append(i)#模拟数据增量流入，保存历史数据
    m.append(t_now)#模拟数据增量流入，保存历史数据
    plt.ylim(0.01, 0.03)
    plt.xlim(0, 1000)
    plt.plot(t,m,'-r')
    #plt.pause(0.001)
