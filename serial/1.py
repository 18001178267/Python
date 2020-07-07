# -*- coding:utf-8 -*-
import serial
ser = serial.Serial()
ser.baudrate = 115200  # 设置波特率（这里使用的是stc89c52）
ser.port = 'COM5'  # 端口是COM3
#print(ser)
ser.open()  # 打开串口
#print(ser)
log=0
print(ser.is_open)  # 检验串口是否打开
while(1):
    #print(ser.is_open)  # 检验串口是否打开
    s = ser.read(3)
    #print(s,s[0],s[1],s[2],len(s),type(s),type(s[0]))
    s0='{:08b}'.format(s[0])
    #print(s0)
    s1='{:08b}'.format(s[1])
    #print(s1)
    s2='{:08b}'.format(s[2])
    #print(s2,type(s2))
    final = s1[-1] + s2[1:] + s0[1:]
    fin = final.encode('utf-8')
    fin = int(fin, 2)
    log+= 1
    #print(final,fin)
    print(fin,log)
    #s = s.decode("UTF-8")