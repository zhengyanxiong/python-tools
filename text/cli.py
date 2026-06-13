"""text.cli — pt text <action>"""

import json

import click


def create_cli():
    """文本处理工具（JSON↔CSV、提取、统计等）"""

    @click.group(name="text")
    def grp():
        """文本处理工具（JSON↔CSV、提取、统计等）"""
        pass

    @grp.command("json2csv")
    @click.argument("input_path")
    @click.option("--output", "-o", default=None, help="输出 CSV 文件路径")
    def json2csv_cmd(input_path: str, output: str):
        """JSON 文件转 CSV"""
        from text.core import json_to_csv

        with open(input_path, "r", encoding="utf-8") as f:
            json_str = f.read()
        csv_str = json_to_csv(json_str)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(csv_str)
            click.echo(f"✅ 已转换到 {output}")
        else:
            click.echo(csv_str)

    @grp.command("csv2json")
    @click.argument("input_path")
    @click.option("--output", "-o", default=None, help="输出 JSON 文件路径")
    def csv2json_cmd(input_path: str, output: str):
        """CSV 文件转 JSON"""
        from text.core import csv_to_json

        with open(input_path, "r", encoding="utf-8") as f:
            csv_str = f.read()
        json_str = csv_to_json(csv_str)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(json_str)
            click.echo(f"✅ 已转换到 {output}")
        else:
            click.echo(json_str)

    @grp.command("extract-json")
    @click.argument("input_path")
    @click.option("--output", "-o", default=None, help="输出 JSON 文件路径")
    def extract_json_cmd(input_path: str, output: str):
        """从混合文本中提取 JSON 块"""
        from text.core import extract_json_from_text

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        blocks = extract_json_from_text(text)

        result = json.dumps(blocks, ensure_ascii=False, indent=2)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result)
            click.echo(f"✅ 提取到 {len(blocks)} 个 JSON 块 → {output}")
        else:
            click.echo(result)

    @grp.command("stats")
    @click.argument("input_path")
    def stats_cmd(input_path: str):
        """统计文本行数、词数、字符数"""
        from text.core import text_stats

        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        stats = text_stats(input_path)
        click.echo(f"行数: {stats['lines']}  词数: {stats['words']}  字符数: {stats['chars']}")

    return grp
