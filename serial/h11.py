import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox  # 要使用messagebox先要导入模块
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from tkinter import ttk  # 创建combobox下拉菜单
import requests  # 发送http请求
from bs4 import BeautifulSoup  # 解析html
#import lxml  # 解析器 中文不乱码
import os  # 创建文件夹
import ssl
import urllib.request
import re
from matplotlib.pyplot import MultipleLocator #从pyplot导入MultipleLocator类，这个类用于设置刻度间隔
import time
from math import *
from datetime import datetime
from matplotlib import font_manager # 实例化 font_manager
import numpy as np
import serial
#from sklearn.cluster import KMeans
import threading
import time
import datetime
from queue import Queue
import numpy as np
def draw_array():
    global array
    while 1:
        fig.clf()
        ax1 = fig.add_subplot(111)
        array = np.random.rand(1, 10)
        array = array[0]
        print(array)
        t = array
        x = range(len(array))
        ax1.plot(x, t)
        canvas.draw()
        time.sleep(2)
# 第1步，实例化object，建立窗口mg
mg = tk.Tk()
# 第2步，给窗口的可视化起名字
mg.title('枕木统计')
# 第3步，设定窗口的大小(长 * 宽)
mg.geometry('1200x600')  # 这里的乘是小x

# 第5步，布置顶部控件
framer = tk.Frame(mg)
framer.pack(side='top')

array=[1,2,3,4,5,6,7,8,9,10]
# canvas.draw()

tk.Button(framer, text='校准', command=draw_array).pack(side='left')
framer_draw = tk.Frame(mg)
framer_draw.pack(side='top')
fig = Figure(figsize=(10, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=framer_draw)  # A tk.DrawingArea.
canvas.get_tk_widget().pack()
plt.ion()  #interactive mode on
# 第6步，主窗口循环显示
mg.mainloop()
