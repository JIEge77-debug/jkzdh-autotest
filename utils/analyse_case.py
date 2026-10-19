import allure


@allure.step("1.解析请求数据")
def analyse_case(case):

    """
    解析测试用例数据
    :param case: 测试用例数据
    :return: 解析后的测试用例数据
    """

    method = case["method"]
    url = "http://192.168.10.131:8888/api/private/v1" + case["path"]  # path是最后的后缀
    headers = eval(case["headers"]) if isinstance(case["headers"], str) else None
    params = eval(case["params"]) if isinstance(case["params"], str) else None
    data = eval(case["data"]) if isinstance(case["data"], str) else None
    json = eval(case["json"]) if isinstance(case["json"], str) else None
    files = eval(case["files"]) if isinstance(case["files"], str) else None

    request_data = {

        "method": method,
        "url": url,
        "headers": headers,
        "params": params,
        "data": data,
        "json": json,
        "files": files,

    }

    #需要返回值
    return request_data