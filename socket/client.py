import socket

client = socket.socket() # 有一些默认参数，即可使用ipv4，这一句是声明socket类型和返回socket连接对象
client.connect(("localhost",3000))
while True:
    msg = input("massage:").strip()

    if len(msg)==0:
        continue

    client.send(msg.encode(encoding='utf-8')) # 不能发空的东西

    data = client.recv(1024)
    print(data.decode())

client.close()