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

from datetime import datetime


from matplotlib import font_manager # 实例化 font_manager
my_font = font_manager.FontProperties(family='SimSun', size=12)


import csv  #生成csv文件

path = "aa.csv"
with open(path,'w',newline='') as f:   #newline=''解决输出有空行的现象
    csv_write = csv.writer(f)
    csv_head = ["x轴","y轴","z轴","时间"]
    csv_write.writerow(csv_head)

a,i=1,1

while(a):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    buf=requests.get(url = 'http://115.29.209.155:8080/TFSV1_sensor/vehicle.ak?method=get_sensor_data&imei=866262042534023&endTime=2019-10-22%2014:42:18',headers=headers)
    #buf是response类型，不是str类型；buf.text才是str类型
    #a=isinstance(buf, str)
    #print(a)
    buf=buf.text
    buf=buf[6:71]
    #print(buf)
    buf = re.findall(r'[-]?\d+.?\d+', buf,) # 返回一个list类型数据
    #print(buf)
    #print(len(buf))
    #j=i*100+1

    timer=datetime.now()
    timer=timer.strftime('%H:%M:%S')
    

    with open(path,'a+',newline='') as f:
        csv_write = csv.writer(f)
        data_row = [float(buf[0]),float(buf[1]),float(buf[2]),timer]
        csv_write.writerow(data_row)

    i=i+1
    print(timer,"done")
    time.sleep(1)

