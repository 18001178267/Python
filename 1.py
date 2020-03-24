import requests  # 发送http请求
import re 
import time 
from datetime import datetime, timedelta #时间的增减
import json #解析本程序list（就是buf）中的str成为dict
import pymssql #sql server
import pymysql #Mysql
import mysql.connector


lastimei=['44659','49963']
#start=input('请输入起始时间（%Y-%m-%d %H:%M:%S）\n')
#end=input('请输入结束时间（%Y-%m-%d %H:%M:%S）\n')



#a,b,m=1,0,0
all_sensor_x=[]
all_sensor_y=[]
all_sensor_z=[]
all_sensor_t=[]

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


def fetch_data(sensor_num):                            #根据输入的传感器编号获取指定设备的X,Y,Z,T数据,并存入整体数组的相应INDEX位置（整体数组是嵌套数组）

    for i in range(sensor_num,(sensor_num+1)):
        all_sensor_data['num_'+str(i)+'_x']=[]
        all_sensor_data['num_'+str(i)+'_y']=[]
        all_sensor_data['num_'+str(i)+'_z']=[]
        all_sensor_data['num_'+str(i)+'_t']=[]


    start = datetime(2019, 11, 4, 21, 47,40) # 用指定日期时间创建datetime
    st=int(start.timestamp()) # 把datetime转换为timestamp
    while((datetime.now().timestamp()-st)>105):
        buf=[]
        strtime=datetime.fromtimestamp(st)
        #print(strtime)
        #fourth_data=strtime.strftime('%H:%M:%S'
        imei='8662620425'+lastimei[sensor_num] 
        buf=send_query(imei,strtime)
        buf=buf.text
        buf=json.loads(buf)
        buf=buf[::-1]   #反转list中数据
        #buf=buf[:2]
        #print(buf)
        #print(type(buf[0]))
        #print(len(buf))

        for j in range(0,len(buf)):
            
            all_sensor_data['num_'+str(sensor_num)+'_x'].append(buf[j]["sensor_1"])
            #print(all_sensor_data['num_'+str(sensor_num)+'_x'])
            #print(type(all_sensor_data['num_'+str(sensor_num)+'_x']))  # list类型
            #print(locals())
            all_sensor_data['num_'+str(sensor_num)+'_y'].append(buf[j]["sensor_2"])
            #print(all_sensor_y['num_'+str(sensor_num)])
            all_sensor_data['num_'+str(sensor_num)+'_z'].append(buf[j]["sensor_3"])
            #print(all_sensor_z['num_'+str(sensor_num)])
            all_sensor_data['num_'+str(sensor_num)+'_t'].append(buf[j]["time"])
            #print(all_sensor_t['num_'+str(sensor_num)])
            #print(len(all_sensor_x['num_'+str(sensor_num)]),len(all_sensor_y['num_'+str(sensor_num)]))
        print("fetch",st,"done")
        
        #print('1x',all_sensor_data['num_'+str(sensor_num)+'_x'])
        #print('1y',all_sensor_data['num_'+str(sensor_num)+'_y'])
        #print('1z',all_sensor_data['num_'+str(sensor_num)+'_z'])
        #print('1t',all_sensor_data['num_'+str(sensor_num)+'_t'])

        st=st+100

def mysql_account():
    #sql服务器名，这里xxx是本地数据库名，也可以用服务器id
    serverName = 'Mysql@localhost:3306'
    #登陆用户名和密码
    userName = 'root'
    passWord = '19940708'
    #建立连接并获取cursor
    #conn = pymysql.connect(serverName, userName , passWord,"magnetic")

    #conn = mysql.connector.connect(user='root', password='19940708', database='magnetic')
    #cursor = conn.cursor()

    #cursor.execute('INSERT INTO Wa (x轴, y轴, z轴, 时间) VALUES (x, y, z, t);')
    #cursor.execute('SELECT * FROM Wa')
    # 创建测试表 persons，包含字段：ID、name、salesrep
    #print(int(len(x)))

def save_mysql_according_to_sensor_num(sensor_num):
    conn = mysql.connector.connect(user='root', password='19940708', database='magnetic')
    cursor = conn.cursor()
    for dt in range(0,int(len( all_sensor_data['num_'+str(sensor_num)+'_x']))):
        #x[dt]=str(x[dt])           
        #y[dt]=str(y[dt])           
        #z[dt]=str(z[dt])           
        #t[dt]=str(t[dt])
        #t[dt] = datetime.strptime(t[dt], '%Y-%m-%d %H:%M:%S.0')
        #t[dt]=t[dt].strftime('%Y-%m-%d %H:%M:%S')
        #print(type(t[dt]))
        sql="INSERT IGNORE INTO imei44659 (x,y,z,data_time) VALUES ("
        sql=sql+ all_sensor_data['num_'+str(sensor_num)+'_x'][dt]+","+ all_sensor_data['num_'+str(sensor_num)+'_y'][dt]+","+ all_sensor_data['num_'+str(sensor_num)+'_z'][dt]+","+"'"+ all_sensor_data['num_'+str(sensor_num)+'_t'][dt]+"'"+")"     #t[dt]两边要用单引号括起来！很重要！！！
        print(sql)
        cursor.execute(sql)
    #cursor.execute('SELECT * FROM imei44659')
    #row = cursor.fetchone()
    #while row:
        #print(row)
        #row = cursor.fetchone()
    #conn.commit()    #从缓存真正写入数据库
    conn.close()



need=input()
need=int(need)
all_sensor_data=globals()

fetch_data(need)
mysql_account()
save_mysql_according_to_sensor_num(need)
