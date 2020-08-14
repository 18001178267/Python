from socket import *
from time import strftime, localtime
from select import select
from json import loads
import os

HOST = '192.168.0.161'
POST = 3000
BUFSIZ = 1024
ADDR = (HOST, POST)

# print(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获得当前目录
# PIC_DIR = os.path.join(BASE_DIR, 'xxx')  # 图片文件夹的路径

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
tcpSerSock.setblocking(False)

inputs = [tcpSerSock]
print('waiting for connnecting...')
while True:
    rlist, wlist, xlist = select(inputs, [], [])

    for s in rlist:
        if s is tcpSerSock:
            tcpCliSock, addr = s.accept()
            print('...connecting from:', addr)
            tcpCliSock.setblocking(False)
            inputs.append(tcpCliSock)
        else:
            data = s.recv(BUFSIZ)

            if not data:
                inputs.remove(s)
                s.close()
                continue

            obj = loads(data.decode('utf-8'))
            time = strftime("%Y-%m-%d %H:%M:%S", localtime())
            data = '[{}]{}: {}'.format(time, obj['name'], obj['msg'])
            for sock in inputs:
                if sock is not tcpSerSock:
                    sock.send(data.encode('utf-8'))
