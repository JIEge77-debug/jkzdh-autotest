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
EXCEL_FILE = "./data/测试用例完整版.xlsx"
# sheet 页作为灵活的变量
SHEET_NAME = "Sheet1"


# MySQL 配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_NAME = "mydb"
DB_USER = "root"
DB_PASSWORD = "your_password"


# ============================================================
# 测试数据清理 SQL（由 conftest.py 在测试前后各执行一次）
#
# 为什么需要：sp_goods 表的 goods_name 有 UNIQUE 唯一约束，
#            而「删除商品」接口只是软删除（is_del=1），记录仍在表里、
#            名字依然被占用，不清理的话第二次跑测试创建同名商品会失败。
#
# 注意：这些 SQL 里的名字要和你 Excel 用例里用的名字保持一致。
#       用 LIKE 'xxx%' 是为了同时覆盖新增和编辑时用到的两个名字。
# ============================================================
SQL1 = "DELETE FROM sp_category WHERE cat_name = '大码服装'"
SQL2 = "DELETE FROM sp_attribute WHERE attr_name = 'VIP尺码'"
SQL3 = "DELETE FROM sp_goods WHERE goods_name LIKE '大码牛仔裤%'"
