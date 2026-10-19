import allure
import jsonpath

from utils.send_request import send_jdbc_request

@allure.step("3.http响应断言")
def http_assert(case,res):
    if case["check"]:
        assert jsonpath.jsonpath(res.json(), case["check"])[0] == case["expected"]
    else:
        assert case["expected"] in res.text


def jdbc_assert(case,):
    if case["sql_check"] and case["sql_expected"]:
        with allure.step("3.jdbc响应断言"):
            assert send_jdbc_request(case["sql_check"]) == case["sql_expected"]