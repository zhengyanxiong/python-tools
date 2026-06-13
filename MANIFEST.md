# Python Tools 脚本清单

> 每次新增脚本后必须更新此清单。

| 模块 | 核心函数 | 功能说明 | CLI 用法 | 额外依赖 |
|------|----------|----------|----------|----------|
| **excel** | `parse_excel`, `excel_to_json`, `generate_excel` | Excel 解析/生成 | `pt excel parse <file>` / `generate <file> --data <json>` | `openpyxl`, `xlrd` |
| **pdf** | `extract_text`, `pdf_to_images` | PDF 文本提取/转图片 | `pt pdf extract <file>` / `to-images <file>` | `pymupdf`, `pdfplumber` |
| **api** | `http_get`, `http_post`, `load_data_ref` | HTTP API 请求 | `pt api get <url>` / `post <url> --data @file` | `httpx` |
| **text** | `json_to_csv`, `csv_to_json`, `extract_json_from_text`, `text_stats` | 文本处理（JSON↔CSV、提取、统计） | `pt text json2csv/csv2json/extract-json/stats` | 无 |
| **encoding** | `encode_file`, `decode_to_file`, `encode_string`, `decode_string` | Base64 编解码 | `pt encoding encode/decode/encode-str/decode-str` | 无（剪贴板需 `pyperclip`） |
| **conversion** | `milliseconds_to_days`, `milliseconds_to_human`, `bytes_to_human` | 数据转换 | `pt conversion ms2days/ms2human/bytes2human` | 无 |
| **db** | `get_table_structures`, `infer_relationships`, `generate_er_diagram` | 数据库 ER 图生成 | `pt db er-diagram --dbname <db>` | `psycopg2`, `sqlalchemy`, `eralchemy2` |
| **file** | `find_files`, `file_hash`, `tree` | 文件操作 | `pt file find/hash/tree` | 无 |
| **media** | `get_media_info` | 媒体文件信息 | `pt media info <file>` | 无 |
| **network** | `check_port`, `dns_lookup` | 网络工具 | `pt network check-port/dns` | 无 |
