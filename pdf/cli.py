"""pdf.cli — pt pdf <action>"""

import click

from common.deps import require


def create_cli():
    """PDF 解析/提取工具"""

    @click.group(name="pdf")
    def grp():
        """PDF 解析/提取工具"""
        pass

    @grp.command("extract")
    @click.argument("file_path")
    @click.option("--pages", default=None, help="页码范围（如 1-5）")
    @click.option("--output", "-o", default=None, help="输出文本文件路径")
    def extract_cmd(file_path: str, pages: str, output: str):
        """提取 PDF 文本内容"""
        require("pdfplumber", "pdf", hint="pip install -r requirements/pdf.txt")
        from pdf.core import extract_text

        text = extract_text(file_path, pages)
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(text)
            click.echo(f"✅ 已提取到 {output}")
        else:
            click.echo(text)

    @grp.command("to-images")
    @click.argument("file_path")
    @click.option("--output-dir", "-o", default="./pdf_images", help="输出目录")
    @click.option("--dpi", default=200, help="图片 DPI")
    def to_images_cmd(file_path: str, output_dir: str, dpi: int):
        """将 PDF 每页转为图片"""
        require("pymupdf", "pdf", hint="pip install -r requirements/pdf.txt")
        from pdf.core import pdf_to_images

        paths = pdf_to_images(file_path, output_dir, dpi)
        click.echo(f"✅ 已生成 {len(paths)} 张图片到 {output_dir}/")

    return grp
