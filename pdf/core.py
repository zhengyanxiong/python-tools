"""pdf.core — PDF 解析/提取核心逻辑"""

from pathlib import Path


def extract_text(file_path: str, pages: str | None = None) -> str:
    """提取 PDF 文本内容。

    Args:
        file_path: PDF 文件路径
        pages: 页码范围（如 "1-5"），None 表示全部

    Returns:
        提取的文本内容
    """
    import pdfplumber

    page_list = _parse_page_range(pages)
    texts = []
    with pdfplumber.open(file_path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            if page_list and i not in page_list:
                continue
            text = page.extract_text()
            if text:
                texts.append(text)
    return "\n\n".join(texts)


def pdf_to_images(file_path: str, output_dir: str = ".", dpi: int = 200) -> list[str]:
    """将 PDF 每页转为图片。

    Returns:
        输出图片路径列表
    """
    import fitz  # pymupdf

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    doc = fitz.open(file_path)
    output_paths = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(dpi=dpi)
        out = str(Path(output_dir) / f"page_{i:03d}.png")
        pix.save(out)
        output_paths.append(out)
    doc.close()
    return output_paths


def _parse_page_range(pages: str | None) -> list[int] | None:
    """解析页码范围字符串，如 '1-5' -> [1,2,3,4,5]。"""
    if not pages:
        return None
    result = []
    for part in pages.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            result.extend(range(int(start), int(end) + 1))
        else:
            result.append(int(part))
    return result or None
