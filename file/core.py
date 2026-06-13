"""file.core — 文件操作核心逻辑"""

import hashlib
import os
import shutil
from pathlib import Path


def find_files(directory: str, pattern: str = "*", max_depth: int = 0) -> list[str]:
    """查找匹配的文件。

    Args:
        directory: 搜索目录
        pattern: glob 匹配模式
        max_depth: 最大深度（0=无限制）

    Returns:
        匹配文件的路径列表
    """
    root = Path(directory)
    if max_depth <= 0:
        return [str(p) for p in root.rglob(pattern) if p.is_file()]

    results = []
    for p in root.rglob(pattern):
        if not p.is_file():
            continue
        depth = len(p.relative_to(root).parts) - 1
        if depth <= max_depth:
            results.append(str(p))
    return sorted(results)


def file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """计算文件哈希值。"""
    h = hashlib.new(algorithm)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dir(path: str) -> str:
    """确保目录存在。"""
    os.makedirs(path, exist_ok=True)
    return path


def tree(directory: str, max_depth: int = 3, prefix: str = "") -> str:
    """生成目录树字符串。"""
    root = Path(directory)
    lines = [root.name + "/"]
    entries = sorted(root.iterdir(), key=lambda p: (not p.is_dir(), p.name))

    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{entry.name}")

        if entry.is_dir() and max_depth > 1:
            extension = "    " if is_last else "│   "
            sub = tree(str(entry), max_depth - 1, prefix + extension)
            lines.extend(sub.split("\n")[1:])

    return "\n".join(lines)
