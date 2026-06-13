"""media.core — 媒体处理核心逻辑（占位，按需扩展）"""


def get_media_info(file_path: str) -> dict:
    """获取媒体文件基本信息（大小、格式等）。"""
    from pathlib import Path

    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    suffix = p.suffix.lower()
    size = p.stat().st_size

    info = {
        "name": p.name,
        "path": str(p.resolve()),
        "size_bytes": size,
        "suffix": suffix,
        "type": _guess_type(suffix),
    }
    return info


def _guess_type(suffix: str) -> str:
    """根据后缀猜测媒体类型。"""
    image_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"}
    audio_exts = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a"}
    video_exts = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".flv"}

    if suffix in image_exts:
        return "image"
    if suffix in audio_exts:
        return "audio"
    if suffix in video_exts:
        return "video"
    return "unknown"
