"""
    ftp 文件客户端
"""
import sys
from socket import *
from time import sleep


# 具体功能
class FtpClient:
    """
        具体功能
    """

    def __init__(self, sockfd):
        self.sockfd = sockfd

    def do_list(self):
        self.sockfd.send(b"L")  # 发送请求
        # 等待回复
        data = self.sockfd.recv(128).decode()
        # ok表示请求成功
        if data == "OK":
            data = self.sockfd.recv(4096).decode()
            print(data)

    def do_get(self, filename):
        # 发送请求
        self.sockfd.send(("G " + filename).encode())
        # 等待回复
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            fd = open(filename, "wb")
            # 接收内容写入文件
            while True:
                data = self.sockfd.recv(1024)
                if data == b"##":
                    print("get file success")
                    fd.close()
                    break
                fd.write(data)
        else:
            print(data)

    def do_put(self, filename):
        try:
            fd = open(filename, "rb")
        except Exception:
            print("Local file is not found")
            return
        filename = filename.split("/")[-1]
        self.sockfd.send(("P " + filename).encode())
        data = self.sockfd.recv(128).decode()
        if data == "OK":
            while True:
                data = fd.read(1024)
                if not data:
                    sleep(0.1)
                    self.sockfd.send(b"##")
                    fd.close()
                    break
                self.sockfd.send(data)
            print("The file put success")
        else:
            print(data)

    def do_quit(self):
        self.sockfd.send(b"Q")
        self.sockfd.close()
        sys.exit("Thank of your use")


# 发起请求
def request(sockfd):
    ftp = FtpClient(sockfd)
    print("\n+——————————————————————+")
    print("|        list          |")
    print("|      get file        |")
    print("|      put file        |")
    print("|        quit          |")
    print("+——————————————————————+")
    while True:
        cmd = input("input commend:")
        cmd = cmd.strip()
        if cmd == "list":
            # sockfd.send(cmd.encode())
            ftp.do_list()
        elif cmd[:3] == "get":
            filename = cmd.split()[-1]
            ftp.do_get(filename)
        elif cmd[:3] == "put":
            filename = cmd.split()[-1]
            ftp.do_put(filename)
        elif cmd == "quit":
            ftp.do_quit()


# 网络连接
def main():
    # 服务器地址
    ADDR = ("127.0.0.1", 8888)
    sockfd = socket()
    try:
        sockfd.connect(ADDR)
    except Exception as e:
        print("Connect server failed")
        return
    print("""
***********************
   Data  File  Image
***********************
    """)
    cls = input("Input the files kinds:")
    if cls not in ("Data", "File", "Image"):
        print("Sorry input Error!!")
        return
    else:
        sockfd.send(cls.encode())
        request(sockfd)


if __name__ == "__main__":
    main()
