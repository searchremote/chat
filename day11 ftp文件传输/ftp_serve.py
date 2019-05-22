from socket import*
from threading import Thread
import os
from time import sleep

#全局变量
ADDR=('0.0.0.0',8888)
FTP='/home/tarena/ftp/'#文件库路径

#将客户端请求功能封装为类
class FtpServer:
    def __init__(self,connfd,FTP_PATH):
        self.connfd=connfd
        self.path=FTP_PATH

    def do_list(self):
        #获取文件列表
        files=os.listdir(self.path)#获取目录下所有的文件组成一个列表
        if not files:
            self.connfd.send("该文件类别为空".encode())
            return
        else:
            self.connfd.send(b'OK')
            sleep(0.1)
        fs=''
        for file in files:
            if file[0]!='.'and \
                os.path.isfile(self.path+file):#是普通文件不是隐藏文件
                fs+=file+'\n'
        self.connfd.send(fs.encode())
    def do_get(self,filename):
        try:
            fd=open(self.path+filename,'rb')#???
        except Exception:
            self.connfd.send('文件不存在'.encode())
        else:
            self.connfd.send(b'OK')
            sleep(0.1)   #防止沾包
        #发送文件内容
        while True:
            data=fd.read(1024)
            if not data:
                sleep(0.1)
                self.connfd.send(b'##')
                break
            self.connfd.send(data)
    def do_put(self,filename):
        if os.path.exists(self.path+filename):
            self.connfd.send("文件已存在".encode())
            return
        self.connfd.send(b"OK")
        f=open(self.path+filename,'wb')
        #接收文件
        while True:
            data=self.connfd.recv(1024)
            if data=="##":
                break
            f.write(data)
        f.close()


#客户端请求处理函数
def handle(connfd):
    cls=connfd.recv(1024).decode()
    FTP_PATH=FTP+cls+'/'
    ftp=FtpServer(connfd,FTP_PATH)
    while True:
        #接收客户端请求
        data=connfd.recv(1024).decode()
        #如果客户端断开返回data为空
        if not data or data[0]=='Q':
            return
        elif data[0]=='L':
            ftp.do_list()
        elif data[0]=='G':#下载文件
            filename=data.split(' ')[-1]
            ftp.do_get(filename)
        elif data[0]=='P':
            filename = data.split(' ')[-1]
            ftp.do_put(filename)


#网络搭建（封装为函数）
def main():
    s=socket(AF_INET,SOCK_STREAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(10)
    print("listen the port 8888")
    while True:
        try:
            connfd, addr = s.accept()
        except KeyboardInterrupt:
            print("退出服务器")
            return #
        except Exception as e:
            print(e)
            continue
        print("连接的客户端：",addr)
        #创建新的线程处理请求
        t=Thread(target=handle,args=(connfd,))
        t.setDaemon(True)
        t.start()

if __name__=='__main__':
    main()



