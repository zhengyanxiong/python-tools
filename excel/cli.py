"""excel.cli — pt excel <action>"""

import json

import click

from common.deps import require


def create_cli():
    """Excel 解析/生成工具"""

    @click.group(name="excel")
    def grp():
        """Excel 解析/生成工具"""
        pass

    @grp.command("parse")
    @click.argument("file_path")
    @click.option("--sheet", default=None, help="工作表名（默认第一个）")
    @click.option("--output", "-o", type=click.Choice(["table", "json"]), default="table", help="输出格式")
    def parse_cmd(file_path: str, sheet: str, output: str):
        """解析 Excel 文件"""
        require("openpyxl", "excel", hint="pip install -r requirements/excel.txt")
        from excel.core import excel_to_json, parse_excel

        if output == "json":
            data = excel_to_json(file_path, sheet)
            click.echo(json.dumps(data, ensure_ascii=False, indent=2))
        else:
            rows = parse_excel(file_path, sheet)
            for row in rows:
                click.echo("\t".join(str(c) for c in row))

    @grp.command("generate")
    @click.argument("file_path")
    @click.option("--data", required=True, help="JSON 数据文件路径（需包含 headers + rows）")
    def generate_cmd(file_path: str, data: str):
        """生成 Excel 文件"""
        require("openpyxl", "excel", hint="pip install -r requirements/excel.txt")
        from excel.core import generate_excel

        with open(data, "r", encoding="utf-8") as f:
            payload = json.load(f)
        headers = payload["headers"]
        rows = payload["rows"]
        result = generate_excel(file_path, headers, rows)
        click.echo(f"✅ Excel 已生成: {result}")

    return grp
