# ============================================================
# 配置模板
#
# 使用方法：
#   复制本文件为 config.py，再按你的环境修改下面的值
#
#   Windows:  copy config\config.example.py config\config.py
#   Mac/Linux: cp config/config.example.py config/config.py
#
# 注意：config.py 已加入 .gitignore，不会被提交到仓库，
#      所以每个人的本地配置互不影响。
# ============================================================

# 环境基准地址
BASE_URL = "http://127.0.0.1:8888/api/private/v1"

# Excel 格式的测试用例文件
EXCEL_FILE = "./data/测试用例.xlsx"
# sheet 页作为灵活的变量
SHEET_NAME = "Sheet1"


# MySQL 配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "mydb"
DB_USER = "root"
DB_PASSWORD = "your_password"
