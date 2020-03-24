import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox  # 要使用messagebox先要导入模块
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from tkinter import ttk  # 创建combobox下拉菜单
import requests  # 发送http请求
from bs4 import BeautifulSoup  # 解析html
import lxml  # 解析器 中文不乱码
import os  # 创建文件夹
import ssl
import urllib.request
import re
from matplotlib.pyplot import MultipleLocator #从pyplot导入MultipleLocator类，这个类用于设置刻度间隔
import time
from math import *
from datetime import datetime
from matplotlib import font_manager # 实例化 font_manager


# 第1步，实例化object，建立窗口mg
mg = tk.Tk()

# 第2步，给窗口的可视化起名字
mg.title('异常地质监测')

# 第3步，设定窗口的大小(长 * 宽)
#mg.geometry('800x600')  # 这里的乘是小x

framer = tk.Frame(mg)
framer.pack(side='top')
fig = Figure(figsize=(10, 6), dpi=100)
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
t = []
x = []
y = []
z = []
canvas = FigureCanvasTkAgg(fig, master=framer)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack()

# 第5步，创建一个frame，设置底部各类参数
def bottom_setup():
    frameb = tk.Frame(mg)
    frameb.pack(side='bottom')


    number1 = tk.StringVar()
    numberChosen1 = ttk.Combobox(frameb, width=12, textvariable=number1)
    numberChosen1['values'] = (27142, 2, 3)     # 设置下拉列表的值
    numberChosen1.current(0)

    number2 = tk.StringVar()
    numberChosen2 = ttk.Combobox(frameb, width=12, textvariable=number2)
    numberChosen2['values'] = (4, 5, 6)     # 设置下拉列表的值
    numberChosen2.current(1)

    number3 = tk.StringVar()
    numberChosen3 = ttk.Combobox(frameb, width=12, textvariable=number3)
    numberChosen3['values'] = (7, 8, 9)     # 设置下拉列表的值
    numberChosen3.current(2)

    number4 = tk.StringVar()
    numberChosen4 = ttk.Combobox(frameb, width=12, textvariable=number4)
    numberChosen4['values'] = (0, 1, 2)     # 设置下拉列表的值
    numberChosen4.current(1)


    def click1():
        #print(number1.get())
        right_setup(int(number1.get()))

    def click2():
        pass

    def click3():
        pass

    def click4():
        pass

    tk.Label(frameb, text='仪器编号',font='20',bg='green').pack(side='left')
    numberChosen1.pack(side='left')      # 设置其在界面中出现的位置 column代表列 row 代表行
    tk.Button(frameb, text='确定', command=click1).pack(side='left')

    tk.Label(frameb, text='异常仪器个数',font='20',bg='green').pack(side='left')
    numberChosen2.pack(side='left')      # 设置其在界面中出现的位置 column代表列 row 代表行
    tk.Button(frameb, text='确定', command=click2).pack(side='left')

    tk.Label(frameb, text='异常持续时间',font='20',bg='green').pack(side='left')
    numberChosen3.pack(side='left')      # 设置其在界面中出现的位置 column代表列 row 代表行
    tk.Button(frameb, text='确定', command=click3).pack(side='left')

    tk.Label(frameb, text='异常阈值',font='20',bg='green').pack(side='left')
    numberChosen4.pack(side='left')      # 设置其在界面中出现的位置 column代表列 row 代表行
    tk.Button(frameb, text='确定', command=click4).pack(side='left')

bottom_setup()

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

def right_setup(machine_num):
    while(1):
        imei='8662620425'+str(machine_num)
        #fig.clf()
        strtime=datetime.now()
        buf=send_query(imei,strtime)
        buf=buf.text
        buf=buf[6:71]
        buf = re.findall(r'[-]?\d+.?\d+', buf,) # 返回一个list类型数据
        timer=datetime.now()
        timer=timer.strftime('%H:%M:%S')

        t.append(timer)
        x.append(float(buf[0]))#模拟数据增量流入x，保存历史数据
        y.append(float(buf[1]))#模拟数据增量流入y，保存历史数据
        z.append(float(buf[2]))#模拟数据增量流入z，保存历史数据
        #print(x,y,z,t)
        try:

            x_major_locator=MultipleLocator(60)
            #把x轴的刻度间隔设置为60，并存在变量里
            ax=fig.gca()
            #ax为两条坐标轴的实例
            ax.xaxis.set_major_locator(x_major_locator)
            #把x轴的主刻度设置为1的倍数
            l1, = ax1.plot(t, x)
        except:
            pass
        try:
            l2, = ax2.plot(t, y)
        except:
            pass
        try:
            l3, = ax3.plot(t, z)
        except:
            pass
        time.sleep(1)
        #canvas = FigureCanvasTkAgg(fig, master=framer)  # A tk.DrawingArea.
        canvas.draw()
        #canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 第6步，主窗口循环显示
mg.mainloop()
