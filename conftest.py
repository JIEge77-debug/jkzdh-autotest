"""
pytest 全局配置文件（注意：文件名必须是 conftest.py，pytest 才会自动加载）

作用：
    在测试开始前、结束后，各清理一次测试数据。

为什么需要清理：
    sp_goods 表的 goods_name 有 UNIQUE 唯一约束，而接口的「删除商品」
    只是软删除（is_del=1），记录仍然留在表里，名字依然被占用。
    如果不清理，第二次跑测试创建同名商品就会失败。
"""
import pymysql
import pytest

from config.config import (
    DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD,
    SQL1, SQL2, SQL3,
)


def _destroy():
    """执行配置里的清理 SQL"""
    sqls = [SQL1, SQL2, SQL3]
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        charset="utf8",
        autocommit=True,
    )
    cur = conn.cursor()
    try:
        for sql in sqls:
            cur.execute(sql)
    finally:
        cur.close()
        conn.close()


@pytest.fixture(scope="session", autouse=True)
def destroy_data():
    # ---- setup：测试开始前先清一次，保证从干净数据起步 ----
    _destroy()

    yield

    # ---- teardown：测试结束后再清一次，留给下一轮干净环境 ----
    _destroy()
