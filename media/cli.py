"""media.cli — pt media <action>"""

import json

import click


def create_cli():
    """媒体处理工具（文件信息等）"""

    @click.group(name="media")
    def grp():
        """媒体处理工具（文件信息等）"""
        pass

    @grp.command("info")
    @click.argument("file_path")
    @click.option("--output", "-o", type=click.Choice(["text", "json"]), default="text")
    def info_cmd(file_path: str, output: str):
        """获取媒体文件信息"""
        from media.core import get_media_info

        info = get_media_info(file_path)
        if output == "json":
            click.echo(json.dumps(info, ensure_ascii=False, indent=2))
        else:
            for k, v in info.items():
                click.echo(f"{k}: {v}")

    return grp
