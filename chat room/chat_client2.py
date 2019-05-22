from socket import*
import os,sys
ADDR=("127.0.0.1",6300)
#发送消息
def send_msg(s,name):
    while True:
        try:
            text=input("发言：")
        except KeyboardInterrupt:
            text="quit"
        if text=="quit":
            ms="Q "+name
            s.sendto(ms.encode(),ADDR)
            sys.exit("退出聊天室")
        msg="C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)
#接收消息
def recv_msg(s):
    while True:
        data,addr=s.recvfrom(1024)
        if data.decode()=="EXIT":
            sys.exit()
        print(data.decode())
#搭建网络连接
def main():
    s=socket(AF_INET,SOCK_DGRAM)
    while True:
        name=input("请输入姓名：")
        msg="L "+name
        s.sendto(msg.encode(),ADDR)
        data,addr=s.recvfrom(1024)
        if data.decode()=="OK":
            print("已进入聊天室")
            break
        else:
            print(data.decode())
    #创建新的进程
    pi=os.fork()
    if pi<0:
        sys.exit("error")
    elif pi==0:
        send_msg(s,name)
    else:
        recv_msg(s)

if __name__=="__main__":
    main()

