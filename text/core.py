"""text.core — 文本处理核心逻辑"""

import csv
import io
import json


def json_to_csv(json_str: str) -> str:
    """将 JSON 数组转换为 CSV 字符串。"""
    data = json.loads(json_str)
    if not data:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def csv_to_json(csv_str: str) -> str:
    """将 CSV 字符串转换为 JSON 数组。"""
    reader = csv.DictReader(io.StringIO(csv_str))
    data = [row for row in reader]
    return json.dumps(data, ensure_ascii=False, indent=2)


def extract_json_from_text(text: str) -> list[str]:
    """从混合文本中提取所有 JSON 块（```json ... ``` 或裸 JSON）。"""
    import re

    results = []
    # 匹配 markdown 代码块中的 JSON
    for match in re.finditer(r"```json\s*(.*?)\s*```", text, re.DOTALL):
        results.append(match.group(1))
    # 匹配裸 JSON 对象/数组
    for match in re.finditer(r"(?<!\w)(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})(?!\w)", text, re.DOTALL):
        try:
            json.loads(match.group(1))
            results.append(match.group(1))
        except json.JSONDecodeError:
            pass
    return results


def text_stats(text: str) -> dict:
    """统计文本基本信息：行数、词数、字符数。"""
    lines = text.count("\n") + 1
    chars = len(text)
    words = len(text.split())
    return {"lines": lines, "words": words, "chars": chars}
