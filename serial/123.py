# -*- coding:utf-8 -*-
import numpy as np
import serial
import math

array = []  #10000采样数组
realtime_value = []
ave = 0
var = 0
ser = serial.Serial()
ser.baudrate = 115200  # 设置波特率
ser.port = 'COM5'  # 端口是COM5
ser.open()  # 打开串口
log=0
#print(ser.is_open)  # 检验串口是否打开
while(1):
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
        # 求参考均值
        ave = np.mean(array)
        # 求参考方差
        var = np.var(array)
        print('取样结束')
        print(' 离地距离参考平均值：',ave,'参考方差：', var)
        break

steel_num = 0       #统计枕木总数
up   = 0            #统计上升沿
down = 0            #统计下降沿，一升一降代表经过一个枕木
realvalue = ave
while(1):
    s = ser.read(3)
    s0='{:08b}'.format(s[0])
    s1='{:08b}'.format(s[1])
    s2='{:08b}'.format(s[2])
    final = s1[-1] + s2[1:] + s0[1:]
    fin = final.encode('utf-8')
    fin = int(fin, 2)
    real_ave = ( fin + ave ) / 2
    # if 100 > fin > 0:
    #     if abs(fin-ave)>5 or (0.5*(math.pow((fin-real_ave),2)+math.pow((ave-real_ave),2))) > 5 :
    #         steel_num += 1
    #         print('\r 枕木数量实时统计：',steel_num,'   实时值',fin,'实时绝对差值:',abs(fin-ave),'实时方差:',0.5*(math.pow((fin-real_ave),2)+math.pow((ave-real_ave),2)),end= ' ')
    # else :
    #     ser.flushInput()
    #     continue
    if 100 > fin > 0:
        if fin-realvalue>5 :
            up += 1
            realvalue = fin
        elif fin-realvalue< (-5) :
            down += 1
            realvalue = fin
        else :
            pass
    else :
        ser.flushInput()
        continue

    print('\r 枕木数量实时统计：',int((up+down)/2),'   实时值',fin,'实时绝对差值:',abs(fin-ave),'实时方差:',0.5*(math.pow((fin-real_ave),2)+math.pow((ave-real_ave),2)),end= ' ')






