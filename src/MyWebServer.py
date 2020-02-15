# coding:utf-8
'''
封装为类 HTTPServer
使用socket 编写最基本的web网站
'''
import socket
import re
import sys

from multiprocessing import Process

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"
WSGI_PYTHON_DIR = "./src/wsgipython"

class HTTPServer(object):
    '''
    web服务器
    调用示例代码:
        http_server = HTTPServer()
        http_server.set_port(8000)
        http_server.start()
    '''
    def __init__(self,application):
        """构造函数， application指的是框架的app"""
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) # 允许重复使⽤上次的套接字绑定的port
        self.app = application

    def set_port(self,port):
        self.server_socket.bind(("",port))

    def start_response(self,status,headers):
        '''
        构造响应头
        '''
        response_headers = "HTTP/1.1 " + status + "\r\n"
        for header in headers:
            response_headers +="%s: %s\r\n" % header
        self.response_headers = response_headers

    def handle_client(self,client_socket):
        """
        处理客户端请求
        """
        # 获取客户端请求数据
        request_data = client_socket.recv(1024 )
        print("request data:",request_data)
        request_lines = request_data.splitlines()
        for line in request_lines:
            print(line)
        
        # 解析请求报文
        # 'GET / HTTP/1.1'
        request_start_line = request_lines[0].decode("utf-8")
        # 提取用户请求的文件名(路径url)
        file_name = re.match(r"\w+ +(/[^ ]*) ",request_start_line).group(1)
        method    = re.match(r"(\w+) +/[^ ]* ",request_start_line).group(1)

        # environment dictionary
        env = {
            "PATH_INFO": file_name,
            "METHOD": method
        }
        # 获得响应体
        response_body = self.app(env,self.start_response)
        response = self.response_headers + '\r\n' + response_body
        print("response data：",response)
        
        # 向客户端返回响应数据
        client_socket.send(bytes(response,"utf-8"))
        
        # 关闭客户端连接
        client_socket.close()
   
    def start(self):
        self.server_socket.listen(128)
        while True:
            client_socket,client_address = self.server_socket.accept()
            print("[%s,%s]用户连接上了" % client_address)

            handle_client_process = Process(target=self.handle_client,args=(client_socket,))
            handle_client_process.start()
            client_socket.close()     


def main():
    '''
    web服务启动主程序入口
    '''
    sys.path.insert(1,WSGI_PYTHON_DIR)  #  增加wsgi模块路径到全局搜索路径中

    # 命令行方式启动 框架 MyWebFramework
    if len(sys.argv) < 2 :
        # sys.exit("python MyWebServer.py Module:app")
        # load defult module_name 
        module_name,app_name = "MyWebFramework:app".split(":")
    else:
        # python src/MyWebServer.py  MyWebFramework:app
        module_name,app_name = sys.argv[1].split(":")
        
    # module_name = "MyWebFramework"
    # app_name = "app"
    m   = __import__(module_name)
    app = getattr(m,app_name)

    # 创建服务实例对象，绑定框架，启动服务实例
    http_server = HTTPServer(app)
    http_server.set_port(8000)
    http_server.start()

if __name__ == "__main__":
    main()
