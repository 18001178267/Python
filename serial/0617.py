import tkinter as tk  # 使用Tkinter前需要先导入
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from pylab import *
import numpy as np
import serial
from sklearn.cluster import KMeans
import threading
import time

# 创建一个frame，设置底部各类参数
def bottom_setup():
    frameb = tk.Frame(mg)
    frameb.pack(side='bottom')

    tk.Label(frameb, text='最新枕木距离',font='20',bg='green').pack(side='left')
    initial_distance = tk.Entry(frameb, width=12,textvariable = '')                   #Entry的text和textvariable属性不可以设置Entry的文本
    initial_distance.pack(side = 'left')

    tk.Label(frameb, text='枕木数量统计',font='20',bg='green').pack(side='left')
    total_num = tk.Entry(frameb, width=12,textvariable = '')
    total_num.pack(side = 'left')

    tk.Label(frameb, text='实时距离值',font='20',bg='green').pack(side='left')
    real_distance = tk.Entry(frameb, width=12,textvariable = '')
    real_distance.pack(side = 'left')

    tk.Label(frameb, text='测量总距离/m',font='20',bg='green').pack(side='left')
    total_distance = tk.Entry(frameb, width=12,textvariable = '')
    total_distance.pack(side = 'left')

    tk.Label(frameb, text='运行速度/(m/s)',font='20',bg='green').pack(side='left')
    velocity_ = tk.Entry(frameb, width=12,textvariable = '')
    velocity_.pack(side = 'left')

    return initial_distance,total_num,real_distance,total_distance,velocity_

def initial(ser,array,initialdistance):
    log=1
    while 1:                                   #首次运行需要加载10000个样本数
        s = ser.read(3)
        s0='{:08b}'.format(s[0])
        s1='{:08b}'.format(s[1])
        s2='{:08b}'.format(s[2])
        final = s1[-1] + s2[1:] + s0[1:]
        fin = final.encode('utf-8')
        fin = int(fin, 2)
        if 100 > fin > 0:
            array.append(fin)
            log+= 1
            print('\r',fin,log,end=' ')
        else :
            ser.flushInput()
            continue
        if log > 10000:
            temp = np.array(array)               #将10000个采样点转成array进行KMeans处理
            y = temp.reshape(-1,1)
            km = KMeans(n_clusters=2)
            km.fit(y)
            km.cluster_centers_
            #print(km.cluster_centers_)
            if km.cluster_centers_[0] > km.cluster_centers_[1]:
                max = km.cluster_centers_[0]
                min = km.cluster_centers_[1]
            else :
                min = km.cluster_centers_[0]
                max = km.cluster_centers_[1]
            print(' 离地距离最大值：',max,'离地距离最小值：', min)
            initialdistance.insert(0,int(min))
            break

def start(totalnum,initialdistance,array,threshold,realdistance,total_distance,velocity_,fig_,canvas_):
    #global up,down
    th1=threading.Thread(target=count,args=(totalnum,total_distance,velocity_))
    th2=threading.Thread(target=realtime,args=(initialdistance,totalnum,threshold,realdistance,))
    # th3=threading.Thread(target=update,args=(initialdistance,))
    th4=threading.Thread(target=draw_array,args=())
    th1.start()
    th2.start()
    # th3.start()
    th4.start()

def count(totalnum,totaldistance,velocity_):
    global up,down
    while 1:
        now = totaldistance.get()
        if now == '':
            now = '0'
        v = str(int(0.7*(up+down)/2)-int(now))
        velocity_.delete(0,'end')
        velocity_.insert(0,v)
        totalnum.delete(0,'end')
        totalnum.insert(0,int((up+down)/2))
        totaldistance.delete(0,'end')
        totaldistance.insert(0,str(int(0.7*(up+down)/2)))
        time.sleep(1)

def realtime(initialdistance,totalnum,threshold,real_distance):
    compare = int(initialdistance.get())
    global up,down,array
    while 1:
        s = ser.read(3)
        s0='{:08b}'.format(s[0])
        s1='{:08b}'.format(s[1])
        s2='{:08b}'.format(s[2])
        final = s1[-1] + s2[1:] + s0[1:]
        fin = final.encode('utf-8')
        fin = int(fin, 2)
        if 100 > fin > 0:
            array.pop(0)
            array.append(fin)
            if fin-compare < (-1*threshold) :
                down += 1
                compare = fin
            elif fin-compare > threshold :
                up += 1
                compare = fin
            else :
                pass
        else :
            ser.flushInput()
            continue
        #print('\r 枕木数量实时统计：', int((up+down)/2), '   实时值', fin, end= ' ')
        real_distance.delete(0,'end')
        real_distance.insert(0,fin)

def update(initialdistance):
    global array
    while 1:
        temp_ = np.array(array)   #将线程中的10000个采样点转成array进行KMeans处理
        y_ = temp_.reshape(-1,1)
        km = KMeans(n_clusters=2)
        km.fit(y_)
        km.cluster_centers_
        if km.cluster_centers_[0] > km.cluster_centers_[1]:
            max_ = km.cluster_centers_[0]
            min_ = km.cluster_centers_[1]
        else :
            min_ = km.cluster_centers_[0]
            max_ = km.cluster_centers_[1]
        #print(' \n最新离地距离最小值：', min_)
        initialdistance.delete(0,'end')
        # initialdistance.insert(0,float('%.2f' % min_))
        initialdistance.insert(0,int(min_))

        time.sleep(5)

def draw_array():
    global array
    while 1:
        ax1.clear()
        x=range(len(array))
        x=np.array(x)
        y=array
        y=np.array(y)
        ax1.plot(x, y)
        canvas.draw_idle()
        time.sleep(1)

def update_distance(initialdistance):
    global array
    temp_ = np.array(array)   #将线程中的10000个采样点转成array进行KMeans处理
    y_ = temp_.reshape(-1,1)
    km = KMeans(n_clusters=2)
    km.fit(y_)
    km.cluster_centers_
    if km.cluster_centers_[0] > km.cluster_centers_[1]:
        max_ = km.cluster_centers_[0]
        min_ = km.cluster_centers_[1]
    else :
        min_ = km.cluster_centers_[0]
        max_ = km.cluster_centers_[1]
    initialdistance.delete(0,'end')
    initialdistance.insert(0,float('%.2f' % min_))

### ***   主程序   *** ###
ser = serial.Serial()
ser.baudrate = 115200                       # 设置波特率
ser.port = 'COM5'                           # 端口是COM5
ser.open()                                  # 打开串口
array = []                                           #10000初始采样数组
threshold = 4                                        #差值的阈值
steel_num = 0                                        #统计枕木总数
up   = 0                                             #统计上升沿
down = 0                                             #统计下降沿，一升一降代表经过一个枕木
# 第1步，实例化object，建立窗口mg
mg = tk.Tk()
# 第2步，给窗口的可视化起名字
mg.title('枕木统计')
# 第3步，设定窗口的大小(长 * 宽)
mg.geometry('1200x600')  # 这里的乘是小x

# 第4步，布置底部控件
initialdistance,totalnum,real_distance,total_distance,velocity = bottom_setup()

# 第5步，布置顶部控件
framer = tk.Frame(mg)
framer.pack(side='top')

framer_draw = tk.Frame(mg)
framer_draw.pack(side='top')

fig = Figure(figsize=(10, 6), dpi=100)
ax1 = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=mg)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack()
plt.ion()

tk.Button(framer, text='校准', command=lambda: initial(ser,array,initialdistance)).pack(side='left')
tk.Button(framer, text='开始', command=lambda: start(totalnum,initialdistance,array,threshold,real_distance,total_distance,velocity,fig,canvas)).pack(side='left')
tk.Button(framer, text='绘图', command=lambda: draw_array()).pack(side='left')
tk.Button(framer, text='手动更新枕木距离', command=lambda: update_distance(initialdistance)).pack(side='left')

# 第6步，主窗口循环显示
mg.mainloop()
