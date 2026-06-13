"""encoding.core — Base64 编解码核心逻辑（无 CLI 依赖，可独立 import）"""

import base64
import os


def encode_file(file_path: str) -> str:
    """读取文件并返回 Base64 编码字符串。"""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def decode_to_file(b64_string: str, out_path: str) -> str:
    """将 Base64 字符串解码并写入文件，返回输出路径。"""
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(b64_string))
    return out_path


def encode_string(text: str) -> str:
    """将字符串编码为 Base64。"""
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def decode_string(b64_string: str) -> str:
    """将 Base64 字符串解码为原文。"""
    return base64.b64decode(b64_string).decode("utf-8")
