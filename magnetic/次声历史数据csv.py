import requests  # 发送http请求
import re 
import time 
from datetime import datetime, timedelta #时间的增减
import csv  #生成csv文件

path = "cisheng.csv"
#newline=''解决输出有空行的现象
with open(path,'w',newline='') as f:  
    csv_write = csv.writer(f)
    csv_head = ["x轴","y轴","z轴","时间"]
    csv_write.writerow(csv_head)

starttime = datetime(2019, 11, 5, 1, 40, 00) # 用指定日期时间创建datetime
st=int(starttime.timestamp()) # 把datetime转换为timestamp
endtime = datetime(2019, 11, 5, 1, 45, 00) # 用指定日期时间创建datetime
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
                          'endTime': end_time})
    return r1

a,b=1,0
for i in range(st,et):
    strtime=datetime.fromtimestamp(i)
    fourth_data=strtime.strftime('%H:%M:%S')
    buf=send_query(866262042535996,strtime)
    buf=buf.text
    buf=buf[6:20]
    #print(buf)
    buf = re.findall(r'[-]?\d+.?\d+', buf,) # 返回一个list类型数据
    with open(path,'a+',newline='') as f:
        csv_write = csv.writer(f)
        data_row = [float(buf[0])]
        csv_write.writerow(data_row)
    a=a+1
    if a%60==0 :
        b=b+1
        print("fetch",60*b,"done")















        
