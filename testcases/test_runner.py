import allure
import jsonpath
import pymysql
import pytest
import requests
from jinja2 import Template

from utils.allure_utils import allure_test_report_init
from utils.excel_utils import read_excel


class TestRunner:

    #读取测试用例文件中的全部数据，用属性保存即可
    data = read_excel()

    #提取后的数据需要初始化一个全局的属性来保存，可以只用{}空字典
    all = {}

    @pytest.mark.parametrize("case",data)
    def test_case(self,case):


        #引用全局变量all{}  建立测试函数内外 all 变量的对应关系
        all = self.all

        #根据all的值，渲染case
        case = eval(Template(str(case)).render(all))
        #初始化allure报告
        allure_test_report_init(case)#意思是形参等于实参 case = case


        #核心步骤1：解析请求数据
        method = case["method"]
        url = "http://192.168.10.131:8888/api/private/v1" + case["path"] #path是最后的后缀
        headers = eval(case["headers"]) if isinstance(case["headers"],str) else None
        params = eval(case["params"]) if isinstance(case["params"],str) else None
        data = eval(case["data"]) if isinstance(case["data"],str) else None
        json = eval(case["json"]) if isinstance(case["json"],str) else None
        files = eval(case["files"]) if isinstance(case["files"],str) else None

        request_data = {

            "method": method,
            "url": url,
            "headers": headers,
            "params": params,
            "data": data,
            "json": json,
            "files": files,

        }

        #核心步骤2：发起请求，得到相应结果
        res = requests.request(**request_data)
        print(res.json())  # 打印响应结果
        #核心步骤3：处理断言
        #http 响应断言
        if case["check"]:
            assert jsonpath.jsonpath(res.json(),case["check"])[0] == case["expected"]
        else:
            assert case["expected"] in res.text

        #数据库断言

        # print(case["sql_check"])
        # print(case["sql_expected"])
        if case["sql_check"] and case["sql_expected"]:
            #连接
            conn = pymysql.connect(
                host="192.168.10.131",
                port=3306,
                database="mydb",
                user="root",
                password="123456",
                charset="utf8"
            )

            #驴+桥
            cur = conn.cursor()
            #执行语句
            cur.execute(case["sql_check"])
            result = cur.fetchone()
            #关闭资源
            cur.close()
            conn.close()
            assert result[0] == case["sql_expected"]

        #核心步骤4：提取
        # JSON提取的功能
        if case["jsonExData"]:

            #首先要把 jsonExData 的 key 和 value拆开
            # 使用eval函数把 case["jsonExData"] 变成字典
            for key,value in eval(case["jsonExData"]).items():
                value = jsonpath.jsonpath(res.json(),value)[0]
                # print(key)
                # print(value)
                all[key] = value


        #数据库的提取
        if case["sqlExData"]:

            for key, value in eval(case["sqlExData"]).items():
                # print(value)
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
                cur.execute(value)
                result = cur.fetchone()
                # 关闭资源
                cur.close()
                conn.close()
                value = result[0]
                # print(value)
                all[key] = value
