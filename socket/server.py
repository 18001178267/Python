from socket import *
from time import ctime

HOST = ''
POST = 3000
BUFSIZ = 1024
ADDR = (HOST, POST)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)  # listen的参数指的是服务器在拒绝新连接前最多接受的未连接数
# tcpSerSock.setblocking(False)

while True:
    print('waiting for connnecting...')

    tcpCliSock, addr = tcpSerSock.accept()
    print(tcpSerSock)

    print(tcpCliSock)
    print('...connecting from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        data = '[{}] {}'.format(ctime(), data.decode('utf-8'))
        tcpCliSock.send(data.encode('utf-8'))

    tcpCliSock.close()
tcpSerSock.close()
