# Python Tools — 可复用工具库

统一 CLI 入口 `pt`，按模块调用子命令。Hermes 执行过程中沉淀的可复用脚本资产。

## 快速开始

```bash
# 安装基础（只装 click）
pip install -e .

# 按需安装模块依赖
pip install -r requirements/excel.txt   # Excel 工具
pip install -r requirements/pdf.txt     # PDF 工具
pip install -r requirements/api.txt     # API 工具
pip install -r requirements/db.txt      # 数据库工具

# 一键安装所有依赖
pip install -r requirements.txt
```

## 使用方式

```bash
pt --help                              # 查看所有模块
pt <module> --help                     # 查看模块用法
pt <module> <action> [options]         # 执行操作
```

## 模块一览

| 模块 | 命令 | 功能 | 额外依赖 |
|------|------|------|----------|
| **excel** | `pt excel parse/generate` | Excel 解析/生成 | `pip install -r requirements/excel.txt` |
| **pdf** | `pt pdf extract/to-images` | PDF 文本提取/转图片 | `pip install -r requirements/pdf.txt` |
| **api** | `pt api get/post` | HTTP API 请求 | `pip install -r requirements/api.txt` |
| **text** | `pt text json2csv/csv2json/extract-json/stats` | 文本处理 | 无 |
| **encoding** | `pt encoding encode/decode/encode-str/decode-str` | Base64 编解码 | 无（剪贴板需 pyperclip） |
| **conversion** | `pt conversion ms2days/ms2human/bytes2human` | 数据转换 | 无 |
| **db** | `pt db er-diagram` | 数据库 ER 图生成 | `pip install -r requirements/db.txt` |
| **file** | `pt file find/hash/tree` | 文件操作 | 无 |
| **media** | `pt media info` | 媒体文件信息 | 无 |
| **network** | `pt network check-port/dns` | 网络工具 | 无 |

## 示例

```bash
# Excel 解析
pt excel parse report.xlsx --sheet Sheet1 --output json
pt excel generate template.xlsx --data data.json

# PDF 提取
pt pdf extract doc.pdf --pages 1-5 --output text
pt pdf to-images doc.pdf --output-dir ./images

# API 请求
pt api get https://api.example.com/data -H "Authorization: Bearer xxx"
pt api post https://api.example.com/submit -d @payload.json

# 文本转换
pt text json2csv data.json --output result.csv
pt text csv2json data.csv --output result.json
pt text extract-json mixed.txt
pt text stats readme.md

# 编解码
pt encoding encode file.bin --clipboard
pt encoding decode file.b64 -o file.bin

# 数据转换
pt conversion ms2days 86400000
pt conversion bytes2human 1073741824

# 文件操作
pt file find . --pattern "*.py" --max-depth 3
pt file hash setup.py --algorithm sha256
pt file tree . --max-depth 2

# 数据库
pt db er-diagram --dbname mydb --user root --output er.png

# 网络
pt network check-port localhost 8080
pt network dns example.com
```

## 项目结构

```
python-tools/
├── pt                    # CLI 统一入口
├── pt_cli/               # CLI 框架
│   ├── main.py           # 入口：注册子命令、路由分发
│   └── registry.py       # 自动发现注册子命令
├── common/               # 公共基础
│   ├── config.py         # 全局配置
│   ├── utils.py          # 通用工具函数
│   └── deps.py           # 可选依赖检查
├── excel/                # Excel 解析/生成
│   ├── cli.py + core.py
├── pdf/                  # PDF 解析/提取
│   ├── cli.py + core.py
├── api/                  # API 请求
│   ├── cli.py + core.py
├── text/                 # 文本处理
│   ├── cli.py + core.py
├── encoding/             # 编解码
│   ├── cli.py + core.py
├── conversion/           # 数据转换
│   ├── cli.py + core.py
├── db/                   # 数据库工具
│   ├── cli.py + core.py
├── file/                 # 文件操作
│   ├── cli.py + core.py
├── media/                # 媒体处理
│   ├── cli.py + core.py
├── network/              # 网络工具
│   ├── cli.py + core.py
├── requirements/         # 分层依赖
│   ├── base.txt
│   ├── excel.txt / pdf.txt / api.txt / db.txt
├── requirements.txt      # 汇总
├── setup.py
├── MANIFEST.md
└── README.md
```

## 新增模块

1. 创建模块目录（如 `ocr/`），包含 `__init__.py`、`cli.py`、`core.py`
2. `cli.py` 中定义 `create_cli()` 返回 click.Group
3. 在 `pt_cli/registry.py` 的 `MODULE_DIRS` 中添加模块名
4. 更新 `MANIFEST.md`、`requirements/`（如有依赖）
5. 提交并推送

## 设计原则

- **cli + core 分离**：`core.py` 纯逻辑可独立 import，`cli.py` 负责命令行交互
- **分层依赖**：基础零依赖，按模块按需安装
- **运行时检查**：缺依赖时友好提示安装命令，不 crash
- **泛化不过拟合**：面向无数场景而非特定测试用例
