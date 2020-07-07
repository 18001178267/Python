# -*- coding:utf-8 -*-
import numpy as np
import serial
from sklearn.cluster import KMeans
import threading
import time
from queue import Queue

def update():
    global compare_distance,array
    while 1:
        temp_ = np.array(array)   #将线程中的10000个采样点转成array进行KMeans处理
        y_ = temp_.reshape(-1,1)
        #print(y,len(y))
        km = KMeans(n_clusters=2)
        km.fit(y_)
        km.cluster_centers_
        #print(km.cluster_centers_)
        if km.cluster_centers_[0] > km.cluster_centers_[1]:
            max_ = km.cluster_centers_[0]
            min_ = km.cluster_centers_[1]
        else :
            min_ = km.cluster_centers_[0]
            max_ = km.cluster_centers_[1]
        # print(' 更新取样结束')
        # print(' 最新离地距离最大值：',max_,'最新离地距离最小值：', min_)
        print(' \n最新离地距离最小值：', min_)
        compare_distance = min_                      #将离地最小值单独取出来，用作与实时值实时比较
        time.sleep(5)

def realtime(ser):
    global up,down,compare_distance,array,threshhold
    while(1):
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
            if fin-compare_distance < (-1*threshhold) :
                down += 1
                compare_distance = fin
            elif fin-compare_distance > threshhold :
                up += 1
                compare_distance = fin
            else :
                pass
        else :
            ser.flushInput()
            continue
        print('\r 枕木数量实时统计：', int((up+down)/2), '   实时值', fin, end= ' ')

array = []                                  #10000初始采样数组
ser = serial.Serial()
ser.baudrate = 115200                       # 设置波特率
ser.port = 'COM5'                           # 端口是COM5
ser.open()                                  # 打开串口
log=1
threshhold = 4
# res = Queue()
# print(ser.is_open)                         # 检验串口是否打开
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
        print(km.cluster_centers_)
        if km.cluster_centers_[0] > km.cluster_centers_[1]:
            max = km.cluster_centers_[0]
            min = km.cluster_centers_[1]
        else :
            min = km.cluster_centers_[0]
            max = km.cluster_centers_[1]
        print(' 初始取样结束')
        print(' 离地距离最大值：',max,'离地距离最小值：', min)
        break

steel_num = 0                                        #统计枕木总数
up   = 0                                             #统计上升沿
down = 0                                             #统计下降沿，一升一降代表经过一个枕木
compare_distance = min                               #将离地最大值单独取出来，用作与实时值实时比较

t1 = threading.Thread(target=update, args=())        #更新距离实时值
t2 = threading.Thread(target=realtime, args=(ser,))  #获取距离实时值
t1.start()
t2.start()
t1.join()
t2.join()







