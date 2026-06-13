"""conversion.cli — pt conversion <action>"""

import click


def create_cli():
    """数据转换工具（时间、大小等）"""

    @click.group(name="conversion")
    def grp():
        """数据转换工具（时间、大小等）"""
        pass

    @grp.command("ms2days")
    @click.argument("milliseconds", type=float)
    def ms2days_cmd(milliseconds: float):
        """毫秒数转天数"""
        from conversion.core import milliseconds_to_days

        days = milliseconds_to_days(milliseconds)
        click.echo(f"{milliseconds} ms = {days} days")

    @grp.command("ms2human")
    @click.argument("milliseconds", type=float)
    def ms2human_cmd(milliseconds: float):
        """毫秒数转人类可读时间"""
        from conversion.core import milliseconds_to_human

        click.echo(milliseconds_to_human(milliseconds))

    @grp.command("bytes2human")
    @click.argument("size_bytes", type=float)
    def bytes2human_cmd(size_bytes: float):
        """字节数转人类可读大小"""
        from conversion.core import bytes_to_human

        click.echo(bytes_to_human(size_bytes))

    return grp
