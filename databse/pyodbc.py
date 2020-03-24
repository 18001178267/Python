import pyodbc
import pymssql
 
# 数据库服务器信息
driver = 'SQL Server Native Client 12.0'  # 因版本不同而异
server = 'local'  
user = 'YZW123'
password = '19940708'
database = 'Wa'
 
conn = pyodbc.connect(driver=driver, server=server, user=user, password=password, database=database)
 
cur = conn.cursor()
sql = 'select * from [checks]'  # 查询语句
cur.execute(sql)
rows = cur.fetchall()  # list
conn.close()
 
for row in rows:
    print(row)  # tuple
