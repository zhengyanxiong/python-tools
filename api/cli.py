"""api.cli — pt api <action>"""

import json

import click

from common.deps import require


def create_cli():
    """HTTP API 请求工具"""

    @click.group(name="api")
    def grp():
        """HTTP API 请求工具"""
        pass

    @grp.command("get")
    @click.argument("url")
    @click.option("--header", "-H", multiple=True, help="请求头（格式: Key: Value）")
    @click.option("--param", "-p", multiple=True, help="查询参数（格式: key=value）")
    @click.option("--output", "-o", default=None, help="输出文件路径")
    def get_cmd(url: str, header: tuple, param: tuple, output: str):
        """发送 GET 请求"""
        require("httpx", "api", hint="pip install -r requirements/api.txt")
        from api.core import http_get

        headers = _parse_headers(header)
        params = _parse_params(param)
        result = http_get(url, headers=headers, params=params)
        _output_result(result, output)

    @grp.command("post")
    @click.argument("url")
    @click.option("--data", "-d", default=None, help="请求体（@file.json 读取文件）")
    @click.option("--header", "-H", multiple=True, help="请求头（格式: Key: Value）")
    @click.option("--output", "-o", default=None, help="输出文件路径")
    def post_cmd(url: str, data: str, header: tuple, output: str):
        """发送 POST 请求"""
        require("httpx", "api", hint="pip install -r requirements/api.txt")
        from api.core import http_post, load_data_ref

        headers = _parse_headers(header)
        json_data = None
        raw_data = None
        if data:
            raw = load_data_ref(data)
            try:
                json_data = json.loads(raw)
            except json.JSONDecodeError:
                raw_data = raw
        result = http_post(url, data=raw_data, json_data=json_data, headers=headers)
        _output_result(result, output)

    return grp


def _parse_headers(header_tuple: tuple) -> dict:
    result = {}
    for h in header_tuple:
        key, _, value = h.partition(":")
        result[key.strip()] = value.strip()
    return result


def _parse_params(param_tuple: tuple) -> dict:
    result = {}
    for p in param_tuple:
        key, _, value = p.partition("=")
        result[key.strip()] = value.strip()
    return result


def _output_result(result: dict, output: str | None):
    body = result["body"]
    text = json.dumps(body, ensure_ascii=False, indent=2) if isinstance(body, dict) else str(body)
    status = result["status"]

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
        click.echo(f"✅ HTTP {status} → {output}")
    else:
        click.echo(f"HTTP {status}")
        click.echo(text)
