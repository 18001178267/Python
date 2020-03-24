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

from datetime import datetime


plt.ion() #开启interactive mode 成功的关键函数
plt.figure()
x = []
y = []
a,i=1,0

def send_query(imei, end_time):
    """
    :param imei: string as 15-digits number
    :param end_time: string in datetime format '%Y-%m-%d %H:%M:%S'
    :return: Response object
    """
    r1 = requests.get(url='http://115.29.209.155:8080/TFSV1_sensor/vehicle.ak?',
                      params={
                          'method': 'get_sensor_data',
                          'imei': imei,
                          'endTime': end_time})
    return r1

while(a):
    plt.clf() #清空画布上的所有内容
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    #buf=requests.get(url = 'http://115.29.209.155:8080/TFSV1_sensor/vehicle.ak?method=get_sensor_data&imei=866262042535996&endTime=2019-10-25%2016:03:00',headers=headers)
    imei='866262042535996'
    strtime=datetime.now()
    buf=send_query(imei,strtime)
    #buf是response类型，不是str类型；buf.text才是str类型
    #a=isinstance(buf, str)
    #print(a)
    buf=buf.text
    #print(buf)
    buf = re.findall(r'sensor_1.?.?.?.?.?\d.?\d+', buf) # 返回一个list类型数据
    #print(buf)
    #print(len(buf))
    j=i*100+1
    for z in buf:#x是str类型
        sensor_1_data= z[11:]
        #print(sensor_1_data)
        x.append(j)#模拟数据增量流入x，保存历史数据
        y.append(float(sensor_1_data))#模拟数据增量流入y，保存历史数据
        j=j+1
    #plt.ylim(-0.5, 0.5)
    plt.xlim(0, 20000)
    plt.plot(x,y,'-r',linewidth=0.1)
    i=i+1
    plt.pause(1)
    
