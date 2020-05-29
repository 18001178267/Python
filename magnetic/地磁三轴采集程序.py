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

lastimei=input('请输入设备IMEI\n')

plt.ion() #开启interactive mode 成功的关键函数
plt.figure()
t = []
x = []
y = []
z = []
a,i=1,1
x_scale=5 #设置X轴刻度

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
    imei=''+lastimei
    strtime=datetime.now()
    buf=send_query(imei,strtime)
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
    
    x.append(float(buf[0]))#模拟数据增量流入x，保存历史数据
    y.append(float(buf[1]))#模拟数据增量流入y，保存历史数据
    z.append(float(buf[2]))#模拟数据增量流入z，保存历史数据

    t.append(timer)
    
    plt.subplot(311)
    #plt.ylim(0, 0.1)
    #plt.xlim(0, 20000)
    plt.title('地磁三轴', fontproperties=my_font)        #设置字体
    plt.plot(t,x,'-r',linewidth=1)
    x_major_locator=MultipleLocator(60)
    #把x轴的刻度间隔设置为60，并存在变量里
    ax=plt.gca()
    #ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    #把x轴的主刻度设置为1的倍数
    
    plt.subplot(312)
    #plt.ylim(0, 0.1)
    #plt.xlim(0, 20000)
    plt.plot(t,y,'-r',linewidth=1)
    y_major_locator=MultipleLocator(60)
    #把y轴的刻度间隔设置为60，并存在变量里
    ay=plt.gca()
    #ay为两条坐标轴的实例
    ay.xaxis.set_major_locator(y_major_locator)
    #把x轴的主刻度设置为1的倍数

    plt.subplot(313)
    #plt.ylim(0, 0.1)
    #plt.xlim(0, 20000)
    plt.xlabel('time')
    plt.plot(t,z,'-r',linewidth=1)
    z_major_locator=MultipleLocator(60)
    #把z轴的刻度间隔设置为60，并存在变量里
    az=plt.gca()
    #ax为两条坐标轴的实例
    az.xaxis.set_major_locator(z_major_locator)
    #把x轴的主刻度设置为1的倍数

    i=i+1

    plt.pause(1)
