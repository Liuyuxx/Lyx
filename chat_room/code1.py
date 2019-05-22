"""
客户端
"""
from socket import *
import struct



HOST = '172.40.71.210'
PORT = 8090
ADDR = (HOST,PORT)


# 创建数据报套接字
sockfd = socket(AF_INET,SOCK_DGRAM)


# 消息收发
with open('client.py','rb') as zxc:
    while True:
        data = zxc.read(1024)
        if not data:
            break
        sockfd.sendto(data,ADDR)


# 关闭套接字
sockfd.close()












