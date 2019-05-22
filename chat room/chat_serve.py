from socket import *
import os,sys
#创建地址
ADDR=("0.0.0.0",6300)
user={}
#进入聊天室
def do_login(s,name,addr):
    if name in user or"管理员"in name:
        s.sendto("该用户已存在".encode(),addr)
        return
    s.sendto(b"OK",addr)
    #通知其他人
    for i in user:
        s.sendto(("欢迎%s来到聊天室"%name).encode(),user[i])
    #将该用户加入聊天室
    user[name]=addr
#聊天
def do_chat(s,name,text):
    msg="%s:%s"%(name,text)
    for i in user:
        if i != name:
            s.sendto(msg.encode(),user[i])
#退出聊天室
def do_quit(s,name):
    msg="%s退出聊天室"%name
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b"EXIT",user[i])
    #将用户删除
    del user[name]


#接收各种客户端请求
def do_request(s):
    data,addr=s.recvfrom(1024)
    msg=data.decode().split(" ")
    if msg[0]=="L":
        do_login(s,msg[0],addr)
    elif msg[0]=="C":
        text=" ".join(msg[2:])
        do_chat(s,msg[1],text)
    elif msg[0]=="Q":
        if msg[1] not in user:
            s.sendto(b"EXIT",addr)
            continue
        do_quit(s,msg[1])



#搭建网络连接
def main():
    # 创建套接字
    s=socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    pi=os.fork()
    if pi<0:
        return
    elif pi==0:
        msg=input("管理员消息：")
        msg="C 管理员消息%s"%msg #
        s.sendto(msg.encode(),ADDR)
    else:
        do_request(s)

if __name__=="__main__":
    main()