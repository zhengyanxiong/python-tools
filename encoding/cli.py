"""encoding.cli — pt encoding <action>"""

import click

from common.deps import require


# Create group in a function to avoid click auto-running at import time
def create_cli():
    """编解码工具（base64 等）"""

    @click.group(name="encoding")
    def grp():
        """编解码工具（base64 等）"""
        pass

    @grp.command("encode")
    @click.argument("input_path")
    @click.option("--clipboard", is_flag=True, help="复制结果到剪贴板")
    def encode_cmd(input_path: str, clipboard: bool):
        """编码文件为 Base64 字符串"""
        from encoding.core import encode_file

        result = encode_file(input_path)
        click.echo(result)

        if clipboard:
            require("pyperclip", "encoding", hint="pip install pyperclip")
            import pyperclip
            pyperclip.copy(result)
            click.echo("✅ 已复制到剪贴板")

    @grp.command("decode")
    @click.argument("input_path")
    @click.option("--output", "-o", default=None, help="输出文件路径")
    def decode_cmd(input_path: str, output: str):
        """解码 Base64 文件"""
        from encoding.core import decode_to_file

        out_path = output or input_path
        with open(input_path, "r") as f:
            b64_string = f.read().strip()
        decode_to_file(b64_string, out_path)
        click.echo(f"✅ 已解码到 {out_path}")

    @grp.command("encode-str")
    @click.argument("text")
    def encode_str_cmd(text: str):
        """编码字符串为 Base64"""
        from encoding.core import encode_string

        click.echo(encode_string(text))

    @grp.command("decode-str")
    @click.argument("b64_string")
    def decode_str_cmd(b64_string: str):
        """解码 Base64 字符串"""
        from encoding.core import decode_string

        click.echo(decode_string(b64_string))

    return grp
