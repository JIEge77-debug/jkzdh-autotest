import os

import pytest

#--alluredir ./report/json_report 指定一个目录并生成中间结果
#--clean-alluredir 没次运行会清空中间结果
if __name__ == "__main__":
    pytest.main(["-vs","./testcases/test_runner.py","--alluredir","./report/json_report","--clean-alluredir"])
    os.system("allure generate ./report/json_report -o ./report/html_report --clean")