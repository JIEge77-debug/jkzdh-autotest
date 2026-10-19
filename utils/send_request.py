import allure
import pymysql
import requests


@allure.step("2.发送http请求")
def send_http_request(**request_data):
    res = requests.request(**request_data)
    return res

def send_jdbc_request(sql,index=0):
    conn = pymysql.connect(
        host="192.168.10.131",
        port=3306,
        database="mydb",
        user="root",
        password="123456",
        charset="utf8"
    )

    # 驴+桥
    cur = conn.cursor()
    # 执行语句
    cur.execute(sql)
    result = cur.fetchone()
    # 关闭资源
    cur.close()
    conn.close()
    return result[index]

