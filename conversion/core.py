"""conversion.core — 数据转换核心逻辑（无 CLI 依赖，可独立 import）"""


def milliseconds_to_days(ms: int | float) -> float:
    """将毫秒数转换为天数。"""
    return ms / 1000 / 60 / 60 / 24


def milliseconds_to_human(ms: int | float) -> str:
    """将毫秒数转换为人类可读的时间字符串。"""
    seconds = ms / 1000
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = seconds / 60
    if minutes < 60:
        return f"{minutes:.1f}min"
    hours = minutes / 60
    if hours < 24:
        return f"{hours:.1f}h"
    days = hours / 24
    return f"{days:.1f}d"


def bytes_to_human(size_bytes: int | float) -> str:
    """将字节数转换为人类可读大小。"""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(size_bytes) < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"
