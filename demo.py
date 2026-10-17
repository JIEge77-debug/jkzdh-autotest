import os

import requests

#切换到本文件所在目录，这样下面的 "./file/banana.jpg" 不管从哪儿启动都能找到
os.chdir(os.path.dirname(os.path.abspath(__file__)))

login = {
    "method":"post",
    "url":"http://192.168.10.131:8888/api/private/v1/login",
    "data": {"username": "admin", "password": "123456"}
}
upload_data = {
    "method": "post",
    "url": "http://192.168.10.131:8888/api/private/v1/upload",
    "headers" : None,
    "files": {"file": ("banana.jpg",open("./file/banana.jpg","rb"), "jpg")}
}

#拿token
res1 = requests.request(**login)
token = res1.json()["data"]["token"]
print(token)


# 文件上传
upload_data["headers"] = {"Authorization": token}
#files 对应的值类似于{参数名:元组}
    #参数名 应该是file（API文档中看的）
        #参数值元组(参数1，参数2，参数3)，
        # 参数1是上传服务器时用的文件名，如果没传，测默认用open() 函数中打开的文件的文件名
        # 参数2是用open()函数打开的文件对象，
        # 参数3是文件类型
        #放到数据里面了

res2  = requests.request(**upload_data)
print(res2.json())
