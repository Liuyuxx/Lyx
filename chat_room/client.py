"""
客户端
"""

from socket import *
import os,sys

# 服务器地址:
ADDR = ('172.40.71.234',9000)

def send_msg(s,name):
    while True:
        try:
            text = input("发言:")
        except KeyboardInterrupt:
            text = 'quit'
        if text == "quit":
            msg = "Q "+ name
            s.sendto(msg.encode(),ADDR)

        msg = "C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)

def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        # 服务端发送EXIT让客户端退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode())






# 创建网络连接
def main():
    s = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input("请输入昵称:")
        msg = "L " + name
        s.sendto(msg.encode(),ADDR)
        # 等待回应
        data,addr = s.recvfrom(1024)
        if data.decode() == "OK":
            print("您已进入聊天室")
        else:
            print(data.decode())


        # 创建新的进程
        pid = os.fork()
        if pid < 0:
            sys.exit("Error!")
        elif pid == 0:
            send_msg(s,name)
        else:
            recv_msg(s)







if __name__ == '__main__':
    main()
