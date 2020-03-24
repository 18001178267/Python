import requests  # 发送http请求
import re 
import time 
from datetime import datetime, timedelta #时间的增减
import json #解析本程序list（就是buf）中的str成为dict
import pymssql #sql server
import pymysql #Mysql
import mysql.connector


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
                          'endTime': end_time})
    return r1

a,b,m=1,0,0
x=[]
y=[]
z=[]
t=[]
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
        t.append(buf[j]["time"])
    print("fetch",i,"done")

#sql服务器名，这里DESKTOP-45NST9K是本地数据库名，也可以用服务器id
serverName = 'Mysql@localhost:3306'
#登陆用户名和密码
userName = 'root'
passWord = '19940708'
#建立连接并获取cursor
#conn = pymysql.connect(serverName, userName , passWord,"magnetic")
conn = mysql.connector.connect(user='root', password='19940708', database='magnetic')
cursor = conn.cursor()
#cursor.execute('INSERT INTO Wa (x轴, y轴, z轴, 时间) VALUES (x, y, z, t);')
#cursor.execute('SELECT * FROM Wa')
# 创建测试表 persons，包含字段：ID、name、salesrep
print(int(len(x)))


for dt in range(0,int(len(x))):
    #x[dt]=str(x[dt])           
    #y[dt]=str(y[dt])           
    #z[dt]=str(z[dt])           
    #t[dt]=str(t[dt])
    #t[dt] = datetime.strptime(t[dt], '%Y-%m-%d %H:%M:%S.0')
    #t[dt]=t[dt].strftime('%Y-%m-%d %H:%M:%S')
    #print(type(t[dt]))
    sql="INSERT IGNORE INTO imei44659 (x,y,z,data_time) VALUES ("
    sql=sql+x[dt]+","+y[dt]+","+z[dt]+","+"'"+t[dt]+"'"+")"     #t[dt]两边要用单引号括起来！很重要！！！
    print(sql)
    cursor.execute(sql)

#cursor.execute('SELECT * FROM imei44659')
#row = cursor.fetchone()
#while row:
    #print(row)
    #row = cursor.fetchone()

conn.commit()    #从缓存真正写入数据库
conn.close()


