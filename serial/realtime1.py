# -*- coding:utf-8 -*-
import serial
import numpy as np
import random
from matplotlib import pyplot as plt
import math
import pylab
import time

def thresholding_algo(y,threshold,influence,yp,
                      avgFilterp,stdFilterp,
                      filteredY,windowsize):
    filteredYnew = 0
    signals = 0
    if abs(y - avgFilterp) > threshold * stdFilterp:
        if y > avgFilterp:
            signals = 0
        else:
            signals = 1
        filteredYnew = influence * y + (1 - influence) * filteredY[-1]
        avgFilter = np.mean(filteredY[0:windowsize+1])
        stdFilter = np.std(filteredY[0:windowsize+1])
    else:
        signals = 0
        filteredYnew = y
        avgFilter = np.mean(filteredY[0:windowsize+1])
        stdFilter = np.std(filteredY[0:windowsize+1])
    return signals, filteredYnew, avgFilter, stdFilter

def threshold1(y,threshold,influence,yp,avgFilterp,stdFilterp,filteredY):

    filteredYnew = 0
    signals = 0

    if abs(y - avgFilterp) > threshold * stdFilterp:
        if y > avgFilterp:
            signals = 0
        else:
            signals = 1
        filteredYnew = influence * y + (1 - influence) * filteredY
        avgFilter = 32
        stdFilter = 0.944
    else:
        signals = 0
        filteredYnew = y
        avgFilter = 32
        stdFilter = 0.94
    return signals, filteredYnew, avgFilter, stdFilter




if __name__ == '__main__':
    #计数器
    counter = 0
    # Serial setting
    ser = serial.Serial()
    ser.baudrate = 115200  # 设置波特率（这里使用的是stc89c52）
    ser.port = 'COM5'  # 端口是COM3
    ser.open()  # 打开串口

    # algorithm setting
    windowsize = 0
    y = []      # 读取数据
    number = 0 # total number
    threshold = 1.8
    influence = 0

    signals = []        # 标志位
    filteredY = []      #
    avgFilter = []
    stdFilter = []
    Initialavg = 32.5
    Initialstd = 0.94
    avgFilter.append(Initialavg)
    stdFilter.append(Initialstd)
    while(1):
        print(ser.is_open)  # 检验串口是否打开
        # 读取数据
        s = ser.read(3)
        s0='{:08b}'.format(s[0])
        s1='{:08b}'.format(s[1])
        s2= '{:08b}'.format(s[2])
        final = s1[-1] + s2[1:] + s0[1:]
        fin = final.encode('utf-8')
        fin = int(fin, 2)
        print(fin)

        y.append(fin)
        number=number+1
        #print(y)
        


        if number < 2000 and number > 1 :
            signal,filterY,avg,stdd = threshold1(fin,threshold,influence,y[-2],avgFilter[-1],stdFilter[-1],filteredY[-1])
            signals.append(signal)
            filteredY.append(filterY)
            avgFilter.append(avg)
            stdFilter.append(stdd)
            if number >2 and y[-2] == 0 and y[-1] == 1:
                counter = counter + 1

        elif number > 1999 & number < 5001:
            windowsize = len(filteredY)
            signal, filterY, avg, stdd = thresholding_algo(fin,threshold,influence,y[-2],avgFilter[-1],stdFilter[-1],filteredY,windowsize)
            signals.append(signal)
            filteredY.append(filterY)
            avgFilter.append(avg)
            stdFilter.append(stdd)
            if y[-2] == 0 and y[-1] == 1:
                counter = counter + 1
        elif number > 5000:
            windowsize = 5000
            signal, filterY, avg, stdd = thresholding_algo(fin, threshold, influence, y[-2], avgFilter[-1],stdFilter[-1],filteredY,windowsize)
            y.pop(0)
            signals.pop(0)
            filteredY.pop(0)
            avgFilter.pop(0)
            stdFilter.pop(0)

            signals.append(signal)
            filteredY.append(filterY)
            avgFilter.append(avg)
            stdFilter.append(stdd)
            if y[-2] == 0 and y[-1] == 1:
                counter = counter + 1
        print(counter)

    #print(a)