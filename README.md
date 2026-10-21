# 接口自动化测试框架

基于 **pytest + requests** 搭建的数据驱动接口自动化测试框架，适合初级自动化工程师学习与参考。

测试用例全部维护在 Excel 中，框架负责完成「读取用例 → 渲染变量 → 发送请求 → 断言结果 → 提取参数 → 生成报告」的完整闭环。**新增一条接口测试，只需在 Excel 里加一行，不用改动任何代码。**

---

## 功能特性

- **数据驱动**：测试用例写在 `data/测试用例.xlsx`，代码只负责执行，加用例不改代码
- **变量传递**：基于 Jinja2 模板 + 全局变量池，实现登录 token、新增记录 ID 等动态参数跨用例传递
- **双维度断言**：支持 HTTP 响应断言（JSONPath 取字段比对）与数据库断言（SQL 查询比对）
- **双通道提取**：支持从接口响应（JSONPath）和数据库（SQL）两种来源提取变量，供后续用例复用
- **可视化报告**：接入 Allure，按 feature / story / title 三层组织报告
- **按需执行**：Excel 中的 `is_True` 列控制某条用例是否参与执行
- **配置集中化**：基地址、Excel 路径、数据库连接统一收敛到 `config/config.py`，换环境只改一处
- **日志可追溯**：请求参数、响应文本、断言实际值与预期值、提取结果等关键节点全部落日志，失败可回看

---

## 技术栈

| 组件 | 用途 |
|---|---|
| pytest | 测试框架，负责用例收集与执行 |
| requests | 发送 HTTP 请求 |
| openpyxl | 读取 Excel 测试用例 |
| Jinja2 | 模板渲染，替换 `{{变量}}` 占位符 |
| jsonpath | 从 JSON 响应中提取字段 |
| PyMySQL | 连接 MySQL 做数据库校验 |
| allure-pytest | 生成可视化测试报告 |
| logging（标准库） | 记录执行过程中的关键信息，落盘到 `log/test.log` |

---

## 目录结构

```
.
├── config/
│   ├── config.example.py      # 配置模板（入库，含占位符）
│   └── config.py              # 你的本地配置（已被 .gitignore 忽略，需自己复制）
├── data/
│   └── 测试用例.xlsx          # 测试用例（核心数据源）
├── file/
│   └── banana.jpg             # 文件上传用例的测试素材
├── testcases/
│   └── test_runner.py         # 用例执行引擎：编排整条流水线
├── utils/
│   ├── excel_utils.py         # read_excel()          读取 Excel → list[dict]
│   ├── analyse_case.py        # analyse_case()        拼装请求参数
│   ├── send_request.py        # send_http_request()   发送 HTTP 请求
│   │                          # send_jdbc_request()   执行 SQL 查询
│   ├── asserts.py             # http_assert()         HTTP 响应断言
│   │                          # jdbc_assert()         数据库断言
│   ├── extractor.py           # json_extractor()      从响应提取变量
│   │                          # jdbc_extractor()      从数据库提取变量
│   └── allure_utils.py        # allure_test_report_init()  设置报告层级
├── run.py                     # 入口：执行用例 + 生成 Allure 报告
├── pytest.ini                 # 日志格式与 pytest 配置
└── requirements.txt
```

### 模块职责一览

| 模块 | 核心函数 | 职责 |
|---|---|---|
| `config/config.py` | —（常量模块） | 集中管理 BASE_URL / EXCEL_FILE / SHEET_NAME / DB_* 等配置（**本地文件，不入库**） |
| `config/config.example.py` | —（模板） | 上面的配置模板，供使用者复制后填写自己的环境 |
| `test_runner.py` | `TestRunner.test_case()` | 总指挥，按顺序调用下面各模块 |
| `excel_utils.py` | `read_excel()` | 把 Excel 读成 `list[dict]`，并按 `is_True` 过滤 |
| `analyse_case.py` | `analyse_case()` | 拼 URL、`eval` 转换请求字段，返回 `request_data` |
| `send_request.py` | `send_http_request()` | 发送 HTTP 请求，返回 `Response` |
| | `send_jdbc_request()` | 连接 MySQL，执行 SQL，返回指定列的值 |
| `asserts.py` | `http_assert()` | 用 JSONPath 取值与 `expected` 比对 |
| | `jdbc_assert()` | 执行 `sql_check` 与 `sql_expected` 比对 |
| `extractor.py` | `json_extractor()` | 从响应提取变量写入全局字典 `all` |
| | `jdbc_extractor()` | 从数据库提取变量写入全局字典 `all` |
| `allure_utils.py` | `allure_test_report_init()` | 设置报告的 feature / story / title |

---

## 快速开始

### 1. 环境要求

- Python 3.9+（开发环境为 3.13）
- 被测服务可访问（地址在 `config/config.py` 中配置）
- MySQL 5.7+（仅数据库断言 / 数据库提取需要）
- Allure 命令行（仅生成 HTML 报告需要）

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 生成本地配置文件

仓库里只有配置模板 `config/config.example.py`，先复制一份真正的配置文件（该文件已被 `.gitignore` 忽略，不会上传）：

```bash
# Windows
copy config\config.example.py config\config.py

# Mac / Linux
cp config/config.example.py config/config.py
```

> 如果你是在本地开发（已经在写代码），`config/config.py` 应该已经存在，可跳过这一步。

### 4. 修改配置

打开 `config/config.py`，按你的环境改这几项：

```python
BASE_URL     = "http://127.0.0.1:8888/api/private/v1"   # 被测服务基地址
EXCEL_FILE   = "./data/测试用例.xlsx"                     # 用例文件路径
SHEET_NAME   = "Sheet1"                                  # 工作表名

DB_HOST      = "127.0.0.1"    # 数据库地址
DB_PORT      = 3306
DB_NAME      = "mydb"
DB_USER      = "root"
DB_PASSWORD  = "your_password"
```

> 只做接口断言、不查数据库时，`DB_*` 这几项不会被用到。

### 5. 执行测试

```bash
python run.py
```

`run.py` 会依次完成：执行 pytest 用例 → 输出 Allure 原始结果 → 生成 HTML 报告。

也可以直接用 pytest：

```bash
pytest ./testcases/test_runner.py -vs
```

生成的报告位于 `report/html_report/index.html`，日志位于 `log/test.log`。

---

## 测试用例设计

用例写在 `data/测试用例.xlsx` 的 `Sheet1` 中：

- **第 1 行**：中文表头（供人阅读）
- **第 2 行**：英文字段名（供代码读取）
- **第 3 行起**：实际用例数据

### 字段说明

| 字段 | 说明 |
|---|---|
| `id` / `feature` / `story` / `title` | 用例编号、所属模块、场景、标题（用于报告展示） |
| `method` | 请求方法：get / post / put / delete |
| `path` | 接口路径，会与基地址拼接成完整 URL |
| `headers` / `params` / `data` / `json` / `files` | 请求头、URL 参数、表单数据、JSON 请求体、上传文件 |
| `check` | 响应断言使用的 JSONPath，如 `$..msg`；留空则退化为全文包含匹配 |
| `expected` | 期望值 |
| `sql_check` / `sql_expected` | 数据库断言的 SQL 语句与期望结果 |
| `jsonExData` | 从响应提取变量，格式如 `{"TOKEN":"$..token"}` |
| `sqlExData` | 从数据库提取变量，格式如 `{"ADMIN_NAME":"select ..."}` |
| `is_True` | 是否执行该用例（TRUE 才执行） |

### 当前用例清单

| ID | 方法 | 路径 | 场景 | 默认执行 |
|---|---|---|---|---|
| 1 | POST | /login | 管理员登录成功 | ✅ |
| 2 | GET | /users | 未登录，查询用户列表失败 | ✅ |
| 3 | GET | /users | 携带 token，查询用户列表成功 | ✅ |
| 4 | POST | /users | 添加用户 | — |
| 5 | PUT | /users/{{BOY_ID}}/state/true | 修改用户状态 | — |
| 6 | POST | /upload | 图片上传 | — |

---

## 框架执行流程

每条用例都会走完下面 5 步（由 `testcases/test_runner.py` 编排）：

```
① 渲染 case  → ② 解析请求参数 → ③ 发送请求 → ④ 断言 → ⑤ 提取变量
                      ↓              ↓          ↓          ↓
              analyse_case.py  send_request.py  asserts.py  extractor.py
```

| 步骤 | 代码位置 | 做了什么 |
|---|---|---|
| **① 渲染** | `test_runner.py` | `Template(str(case)).render(all)` 把 `{{TOKEN}}` 这类占位符替换成真实值 |
| **② 解析** | `analyse_case()` | 拼接完整 URL；把 Excel 中的字符串（如 `'{"a": 1}'`）用 `eval` 转成 dict |
| **③ 发送** | `send_http_request()` | `requests.request(**request_data)`，并把请求记录下来供 Allure 展示 |
| **④ 断言** | `http_assert()` / `jdbc_assert()` | HTTP 用 `jsonpath(...)[0] == expected`；数据库用 SQL 查询结果比对 |
| **⑤ 提取** | `json_extractor()` / `jdbc_extractor()` | 把 token、新增记录 ID 等写入全局字典 `all`，供后续用例使用 |

每个工具函数都加了 `@allure.step`，所以在 Allure 报告中能看到「1.解析请求数据 → 2.发送http请求 → 3.http响应断言 → 4.json提取」的完整步骤链。

---

## 变量传递机制

这是框架的核心设计，关键在于 `TestRunner.all` 这个全局字典：

```
用例1 登录 ──> 提取 TOKEN ──> all["TOKEN"] ──┐
                                             ├─> 用例3/4/5 的 headers 写 {{TOKEN}}
用例4 新增 ──> 提取 BOY_ID ──> all["BOY_ID"] ─┤
                                             └─> 用例5 的 path 写 {{BOY_ID}}
```

因此**用例之间存在依赖顺序**：登录用例一旦失败，后续依赖 token 的用例会连锁失败。

---

## Allure 报告

`utils/allure_utils.py` 利用 Excel 中的 `feature` / `story` / `title` 动态生成报告结构，报告可按模块、场景分层查看。

报告中每条用例下会展开 4 个步骤（由各工具函数上的 `@allure.step` 产生）：

```
1.解析请求数据  →  2.发送http请求  →  3.http响应断言 / 3.jdbc响应断言  →  4.json提取 / 4.jdbc提取
```

---

## 日志

日志配置在 `pytest.ini` 中，使用 Python 标准库 `logging`，**同时输出到控制台和文件**：

```ini
log_file = ./log/test.log      # 落盘位置
log_cli  = True                # 同时打印到控制台
```

各模块在关键节点记录日志：

| 位置 | 记录内容 |
|---|---|
| `test_runner.py` | 用例 ID / 模块 / 场景 / 标题 |
| `analyse_case.py` | 解析后的完整 `request_data` |
| `send_request.py` | 响应文本 `res.text` |
| `asserts.py` | 断言的实际值与预期值（HTTP 与 JDBC 各一条） |
| `extractor.py` | 提取之后的全局变量 `all` |

**日志格式**（`pytest.ini` 中配置）：

```
%(asctime)s %(filename)-20s[函数:%(funcName)-18s] [line:%(lineno)-3d]  %(levelname)s --%(message)s
```

输出示例：

```
2026-10-19 21:30:11,203 analyse_case.py     [函数:analyse_case    ] [line:37 ]  INFO --1.解析请求数据，请求数据为:{...}
```

> **排错思路**：先看 `log/test.log` 里断言那两条日志，能直接看到「实际值 vs 预期值」，比翻 Allure 报告快。

---

## 注意事项

1. **本地配置不入库**：真实地址与数据库密码放在 `config/config.py`，该文件已加入 `.gitignore`；仓库里只保留模板 `config/config.example.py`。首次使用请按「快速开始」第 3 步复制模板。若需更高安全性，可进一步改为环境变量读取（`os.getenv("DB_PASSWORD")`）
2. **用例依赖顺序**：变量通过全局字典传递，后置用例依赖前置用例的提取结果，不适合随机顺序执行
3. **新增用户用例的可重复性**：接口对用户名有唯一性约束，重复执行会返回「用户名已存在」，建议用时间戳 / 随机数生成唯一用户名，或增加后置清理逻辑
4. **`eval` 的使用**：为简化 Excel 字符串解析而使用 `eval`，仅适用于可信的本地用例文件

---

## 声明

本项目为个人学习与实践项目，用于学习接口自动化测试框架的设计思路，不作为生产级工具使用。
