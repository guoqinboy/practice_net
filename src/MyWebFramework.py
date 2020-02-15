# coding:utf-8

import time
import sys

# 设置静态文件根目录
HTML_ROOT_DIR = "./html"

class Application(object):
    """
    框架的核心部分，也就是框架的主题程序，框架是通用的
    """

    def __init__(self,urls):
        """
        设置路由信息
        """
        self.urls=urls
    
    def __call__(self,env,start_response):
        path = env.get("PATH_INFO","/")
        #  /static/index.html
        if path.startswith("/static"):
            # 要访问静态文件
            file_name = path[7:]
            # print("file_name=" + file_name)

            # 打开文件，读取内容
            try:
                file = open(HTML_ROOT_DIR + file_name,"rb")
            except IOError:
                # 代表未找到路由信息，404错误
                status  = "404 Not Found"
                headers = []
                start_response(status,headers)
                return "not found"
            else:
                file_data = file.read()
                file.close()

                status  = "200 OK"
                headers = []
                start_response(status,headers)
                return file_data.decode("utf-8") # decode 将二进制数据解析为utf-8字符

        #  路由分发
        for url,handler in self.urls:
              # ("/ctime", show_ctime) 
              if path == url:
                  return handler(env,start_response)

        # 代表未找到路由信息，404错误
        status  = "404 Not Found"
        headers = []
        start_response(status,headers)
        return "not found"


# handle 处理函数
def show_ctime(env,start_response):
    status  = "200 OK"
    headers = [
        ("Content-Type", "text/plain")
    ]
    start_response(status,headers)
    return time.ctime()    

def say_hello(env, start_response):
    status = "200 OK"
    headers = [
        ("Content-Type", "text/plain")
    ]
    start_response(status, headers)
    return u"欢迎来到宜昌！"

# 路由列表
urls = [
            ("/", show_ctime),
            ("/ctime", show_ctime),
            ("/sayhello", say_hello),
        ]

# 实例化对象
app = Application(urls)


