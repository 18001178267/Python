import pymssql
#sql服务器名，这里(127.0.0.1)是本地数据库IP
serverName = 'DESKTOP-45NST9K'
#登陆用户名和密码
userName = 'a'
passWord = '123456'
#建立连接并获取cursor
conn = pymssql.connect(serverName, userName , passWord,"magnetic")
cursor = conn.cursor()
# 创建测试表 persons，包含字段：ID、name、salesrep

x=[1]
x[0]=str(x[0])

y=[1]
y[0]=str(y[0])

z=[1]
z[0]=str(z[0])

t=[1]
t[0]=str(t[0])


sql="INSERT INTO Wa (x,y,z,time) VALUES ("
sql=sql+x[0]+","+y[0]+","+z[0]+","+t[0]+")"
cursor.execute(sql)


cursor.execute('SELECT * FROM Wa')
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()

#conn.commit()
conn.close()
