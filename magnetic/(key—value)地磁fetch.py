import requests  # 发送http请求
import re 
import time 
from datetime import datetime, timedelta #时间的增减
import csv  #生成csv文件
import json #解析本程序list（就是buf）中的str成为dict

lastimei=[49922,36002,44667,36044,26003,42216,27142,34023,44527,36036,49930,27159,25856,
          33918,27134,33900,25930,25906,25872,44659,49963,44592,44626,36069,44576,35970,
          49906,44550,36119,33991,25922,36051,35947,44634,42158,27167,25971,49948,25542,
          49971,33942,25914,25948,33926,27126,49955,42232,34056,25963,25898,34064,34031,
          49898,33934,44642,25849,25864,33959,50003,49914]


#lastimei=input('请输入设备IMEI后5位\n')


start=input('请输入起始时间（%Y-%m-%d %H:%M:%S）\n')
end=input('请输入结束时间（%Y-%m-%d %H:%M:%S）\n')

for overall in range(0,60,1):
    #starttime = datetime(2019, 10, 21, 14, 00, 00) # 用指定日期时间创建datetime
    starttime = datetime.strptime(start,'%Y-%m-%d %H:%M:%S') # 用指定日期时间创建datetime
    st=int(starttime.timestamp()) # 把datetime转换为timestamp
    #endtime = datetime(2019, 10, 21, 14, 20, 00) # 用指定日期时间创建datetime
    endtime = datetime.strptime(end,'%Y-%m-%d %H:%M:%S') # 用指定日期时间创建datetime
    et=int(endtime.timestamp()) # 把datetime转换为timestamp

    name1=starttime.strftime('%Y-%m-%d-%H-%M-%S')
    name2=endtime.strftime('%Y-%m-%d-%H-%M-%S')

    path = str(lastimei[overall]) + '地磁' + str(name1) + ' to ' + str(name2) + '.csv'
    #newline=''解决输出有空行的现象
    with open(path,'w',newline='') as f:  
        csv_write = csv.writer(f)
        csv_head = ["x轴","y轴","z轴"]
        csv_write.writerow(csv_head)

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

    a,b,m=1,0,0
    x=[]
    y=[]
    z=[]
    t=[]
    for i in range(st+100,et+1,1000):
        strtime=datetime.fromtimestamp(i)
        #print(strtime)
        #fourth_data=strtime.strftime('%H:%M:%S')
        imei='8662620425'+str(lastimei[overall])
        buf=send_query(imei,strtime)
        buf=buf.text
        buf=json.loads(buf)
        buf=buf[::-1]   #反转list中数据
        for j in range(0,len(buf)):
            x.append(buf[j]["sensor_1"])
            y.append(buf[j]["sensor_2"])
            z.append(buf[j]["sensor_3"])
        print("fetch",i,"done")


    with open(path,'a+',newline='') as f:
        for m in range(0,int(len(x))):
            csv_write = csv.writer(f)
            data_row = [float(x[m]),float(y[m]),float(z[m])]
            csv_write.writerow(data_row)
