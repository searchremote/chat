from socket import*
import sys,time

#具体功能
class FtpClient:
    def __init__(self,s):
        self.s=s
    def do_list(self):
        self.s.send(b'L')#发送L表示列表
        #等待回复
        data=self.s.recv(4096).decode()
        if data=='OK':#ok表示请求成功
            data1=self.s.recv(4096)
            print(data1.decode())
        else:
            print(data)
    def do_quit(self):
        self.s.send(b'Q')
        self.s.close()
        sys.exit("退出")
    def do_get(self,filename):
        #发送请求
        self.s.send(b'G '+filename.encode())
        #等待回复
        data=self.s.recv(128).decode()
        if data=="OK":
            fd=open(filename,'wb')
            #接收内容写入文件
            while True:
                data1=self.s.recv(1024)
                if data1==b'##':
                    break
                fd.write(data1)
            fd.close()
        else:
            print(data)
    def do_put(self,filename):
        try:
            f=open(filename,'rb')
        except Exception:
            print("没有该文件")
            return
        #发送请求
        filename=filename.split('/')[-1]
        self.s.send(b'P '+filename.encode())
        #等待回复
        data=self.s.recv(128).decode()
        if data=="OK":
            while True:
                data1=f.read(1024)
                if not data:
                    time.sleep(0.1)
                    self.s.send(b"##")
                    break
                self.s.send(data1)
            f.close()
        else:
            print(data)

def request(s):
    ftp=FtpClient(s)
    while True:
        print("\n---------命令选项------------")
        print("########### list #############")
        print("########### get file ###########")
        print("########### put file ###########")
        print("########### quit #############")
        print("------------------------------")
        cmd=input("输入命令:")
        if cmd.strip()=='list':#移除字符串头尾指定的字符（默认为空格）或字符序列
            ftp.do_list()
        elif cmd.strip()=="quit":
            ftp.do_quit()
        elif cmd[:3]=='get':
            filename=cmd.strip().split(' ')[-1]
            ftp.do_get(filename)
        elif cmd[:3] == 'put':
            filename = cmd.strip().split(' ')[-1]
            ftp.do_put(filename)

def main():
    ADDR = ('0.0.0.0', 8888)
    s=socket(AF_INET,SOCK_STREAM)
    try:
        s.connect(ADDR)
    except Exception as e:
        print(e,"连接服务器失败")
        return
    else:
        print("""
        **************************************
        data file img
        **************************************
        """)
        cls=input("请选择文件种类：")
        if cls not in ['data','file','img']:
            print("sorry input error")
            return
        else:
            s.send(cls.encode())
            request(s,)

if __name__=="__main__":
    main()

