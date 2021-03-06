import requests  # 发送http请求
import re 
import time 
from datetime import datetime, timedelta #时间的增减
import csv  #生成csv文件
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

name1=starttime.strftime('%Y-%m-%d-%H-%M-%S')
name2=endtime.strftime('%Y-%m-%d-%H-%M-%S')

path = lastimei + '次声' + str(name1) + ' to ' + str(name2) + '.csv'
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
for i in range(st+2,et+1,2):
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
        #y.append(buf[j]["sensor_2"])
        #z.append(buf[j]["sensor_3"])
    print("fetch",i,"done")


with open(path,'a+',newline='') as f:
    for m in range(0,int(len(x))):
        csv_write = csv.writer(f)
        data_row = [float(x[m])]
        csv_write.writerow(data_row)
