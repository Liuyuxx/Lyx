"""
ftp 文件服务器
并发网络功能训练
"""

from socket import *
from threading import Thread
import sys,os
from time import sleep


# 全局变量
HOST = '0.0.0.0'
PORT = 9000
ADDR = (HOST, PORT)
FTP = '/home/tarena/FTP/'   # 文件库路径


# 将客户端请求功能封装为类
class FtpServer:
    def __init__(self,data,FTP_PATH):
        self.data = data
        self.path = FTP_PATH

    def do_list(self):
        # 获取文件列表
        files = os.listdir(self.path)
        if not files:
            self.data.send("该文件类别为空".encode())
            return
        else:
            self.data.send(b'OK')
            sleep(0.1)

        fs = ''
        for file in files:
            if file[0] != '.' and os.path.isfile(self.path+file):
                fs += file + '\n'

        self.data.send(fs.encode())
        sleep(0.1)
        self.data.send(b"##")

    def do_get(self,filename):
        try:
            fd = open(self.path + filename,'rb')
        except IOError:
            self.data.send("文件不存在".encode())
            return
        else:
            self.data.send(b"OK")
            sleep(0.1)
        # 发送文件内容
        while True:
            nr = fd.read(1024)
            if not nr:
                sleep(0.1)
                self.data.send(b'##')
            self.data.send(nr)


    def do_put(self,filename):
        if os.path.exists(self.path+filename):
            self.data.send("该文件已存在".encode())
            return
        self.data.send(b'OK')
        fd = open(self.path+filename,'wb')
        # 接收文件
        while True:
            nr = self.data.recv(1024)
            if nr == b"##":
                break
            fd.write(nr)
        fd.close()


# 客户端请求处理函数
def handle(data):
    cls = data.recv(1024).decode()
    FTP_PATH = FTP + cls +'/'
    while True:
        ftp = FtpServer(data,FTP_PATH)
        abc = data.recv(1024).decode()

        if not abc or abc[0] == 'Q':
            return
        elif abc[0] == 'L':
            ftp.do_list()
        elif abc[0] == 'G':
            filename = abc.split(" ")[-1]
            ftp.do_get(filename)
        elif abc[0] == 'P':
            filename = abc.split(" ")[-1]
            ftp.do_put(filename)


# 网络搭建
def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)
    print("Listen the port 9000.....")

    # 循环等待客户端连接
    while True:
        try:
            data, addr = sockfd.accept()
        except KeyboardInterrupt:
            print("退出服务程序")
            return
        except Exception as e:
            print(e)
            continue
        # 连接客户端
        print("链接的客户端地址:",addr)
        # 创建新的线程处理客户端请求
        client = Thread(target=handle, args=(data,))
        client.setDaemon(True)  # 分支线程随主线程退出
        client.start()

if __name__ == "__main__":
    main()



