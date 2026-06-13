"""api.core — HTTP API 请求工具核心逻辑"""

import json
from pathlib import Path
from typing import Any


def http_get(
    url: str,
    headers: dict[str, str] | None = None,
    params: dict[str, str] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """发送 GET 请求，返回 {"status": int, "headers": dict, "body": str|dict}。"""
    import httpx

    resp = httpx.get(url, headers=headers, params=params, timeout=timeout)
    body = _parse_body(resp)
    return {"status": resp.status_code, "headers": dict(resp.headers), "body": body}


def http_post(
    url: str,
    data: Any = None,
    json_data: Any = None,
    headers: dict[str, str] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """发送 POST 请求。"""
    import httpx

    resp = httpx.post(url, content=data, json=json_data, headers=headers, timeout=timeout)
    body = _parse_body(resp)
    return {"status": resp.status_code, "headers": dict(resp.headers), "body": body}


def load_data_ref(ref: str) -> str:
    """加载数据引用：@file.json 读取文件内容，否则直接返回。"""
    if ref.startswith("@"):
        path = ref[1:]
        return Path(path).read_text(encoding="utf-8")
    return ref


def _parse_body(resp) -> Any:
    """尝试解析响应体为 JSON，失败则返回文本。"""
    try:
        return resp.json()
    except Exception:
        return resp.text
