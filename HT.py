import requests  # 发送http请求
import re 
import time 
from datetime import datetime, timedelta #时间的增减
import csv  #生成csv文件

#path = "history.csv"
#newline=''解决输出有空行的现象
#with open(path,'w',newline='') as f:  
#    csv_write = csv.writer(f)
#    csv_head = ["x轴","y轴","z轴","时间"]
#    csv_write.writerow(csv_head)

starttime = datetime(2019, 10, 21, 14, 00, 00) # 用指定日期时间创建datetime
st=int(starttime.timestamp()) # 把datetime转换为timestamp
endtime = datetime(2019, 10, 21, 14, 2, 00) # 用指定日期时间创建datetime
et=int(endtime.timestamp()) # 把datetime转换为timestamp

def send_query():
    """
    :param imei: string as 15-digits number
    :param end_time: string in datetime format '%Y-%m-%d %H:%M:%S'
    :return: Response object
    """
    r1 = requests.get(url='http:///oa.haitian.com/workflow/request/ManageRequestNoForm.jsp?',
                      params={
                          'fromFlowDoc': '',
                          'requestid': '1129159',
                          'isrequest': '0',
                          'isovertime': '0',
                          'isaffirmance': '',
                          'reEdit': '1',
                          'seeflowdoc': '0',
                          'isworkflowdoc': '0',
                          'isfromtab' : 'false'})
    return r1

#http://oa.haitian.com/workflow/request/ManageRequestNoForm.jsp?fromFlowDoc=&requestid=1129159&isrequest=0&isovertime=0&isaffirmance=&reEdit=1&seeflowdoc=0&isworkflowdoc=0&isfromtab=false


#strtime=datetime.fromtimestamp(i)
#fourth_data=strtime.strftime('%H:%M:%S')
buf=send_query()
buf=buf.text
print(buf)
"""
buf=buf[6:71]
        buf = re.findall(r'[-]?\d+.?\d+', buf,) # 返回一个list类型数据
        with open(path,'a+',newline='') as f:
            csv_write = csv.writer(f)
            data_row = [float(buf[0]),float(buf[1]),float(buf[2]),fourth_data]
            csv_write.writerow(data_row)
        a=a+1
        if a%60==0 :
            b=b+1
            print("fetch",60*b,"done")
"""















        
