import requests  # 发送http请求
from bs4 import BeautifulSoup  # 解析html
import lxml  # 解析器 中文不乱码
import os  # 创建文件夹
import ssl

import urllib.request
import re

import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator #从pyplot导入MultipleLocator类，这个类用于设置刻度间隔
import numpy as np
import time
from math import *

#plt.ion() #开启interactive mode 成功的关键函数
plt.figure()
t = [0]
t2= [0]
y = [0]
y2= [0]

for i in range(1,2000):
    plt.clf() #清空画布上的所有内容
    plt.subplot(211)
    t.append(i)#模拟数据增量流入，保存历史数据
    y.append(i)#模拟数据增量流入，保存历史
    plt.plot(t,y,'-r')
    plt.subplot(212)
    if i<10:
        t2.append(i)#模拟数据增量流入，保存历史数据
        y2.append(i)#模拟数据增量流入，保存历史
        plt.plot(t2,y2,'-r')
    else:
        t2.append(i)#模拟数据增量流入，保存历史数据
        y2.append(i)#模拟数据增量流入，保存历史数据
        plt.plot(t2,y2,'-r')
        plt.xlim(i-5,i)
    plt.pause(0.5)
