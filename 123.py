import tkinter as tk  # 使用Tkinter前需要先导入
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from pylab import *   #包含Figure（），鬼知道具体在哪个包

import requests  # 发送http请求 
import time 
from datetime import datetime, timedelta #时间的增减
import json #解析本程序list（就是buf）中的str成为dict

lastimei=input('请输入设备IMEI后5位\n')
start=input('请输入起始时间（%Y-%m-%d %H:%M:%S）\n')
end=input('请输入结束时间（%Y-%m-%d %H:%M:%S）\n')


#starttime = datetime(2019, 10, 21, 14, 00, 00) # 用指定日期时间创建datetime
starttime = datetime.strptime(start,'%Y-%m-%d %H:%M:%S') # 用指定日期时间创建datetime
st=int(starttime.timestamp()) # 把datetime转换为timestamp
#endtime = datetime(2019, 10, 21, 14, 20, 00) # 用指定日期时间创建datetime
endtime = datetime.strptime(end,'%Y-%m-%d %H:%M:%S') # 用指定日期时间创建datetime
et=int(endtime.timestamp()) # 把datetime转换为timestamp

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
                          'endTime': end_time}，timeout = 5)
    return r1

def fetch():
    for i in range(st+100,et+1,100):
        strtime=datetime.fromtimestamp(i)
        #print(strtime)
        #fourth_data=strtime.strftime('%H:%M:%S')
        imei='8662620425'+lastimei
        buf=send_query(imei,strtime)
        buf=buf.text
        buf=json.loads(buf)
        buf=buf[::-1]   #反转list中数据
        for j in range(0,len(buf)):
            x.append(buf[j]["sensor_1"])
            y.append(buf[j]["sensor_2"])
            z.append(buf[j]["sensor_3"])
        print("fetch",i,"done")

# 第1步，实例化object，建立窗口window
window = tk.Tk()
 
# 第2步，给窗口的可视化起名字
window.title('异常地质监测')
 
# 第3步，设定窗口的大小(长 * 宽)
window.geometry('800x600')  # 这里的乘是小x
 

fig = Figure(figsize=(30, 30), dpi=100)
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)

x = np.arange(-5.0, 5.0, 0.02)
   
y_s1 = np.sin(x)
y_s2 = np.sin(x*2)
y_s3 = np.sin(x*3)

 # initialize drawing
try:
    l1, = ax1.plot(x, y_s1)
except:
    pass
try:
    l2, = ax2.plot(x, y_s2)
except:
    pass
try:
    l3, = ax3.plot(x, y_s3)
except:
    pass
canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


# 第6步，主窗口循环显示
window.mainloop()
