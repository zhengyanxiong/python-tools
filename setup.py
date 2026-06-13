from setuptools import setup, find_packages

setup(
    name="python-tools",
    version="0.1.0",
    description="可复用 Python 工具库 — 统一 CLI 入口 pt",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "click>=8.0",
    ],
    extras_require={
        "excel": ["openpyxl>=3.0", "xlrd>=2.0"],
        "pdf": ["pymupdf>=1.23", "pdfplumber>=0.9"],
        "api": ["httpx>=0.24"],
        "db": ["psycopg2-binary", "sqlalchemy>=2.0", "eralchemy2"],
        "all": [
            "openpyxl>=3.0", "xlrd>=2.0",
            "pymupdf>=1.23", "pdfplumber>=0.9",
            "httpx>=0.24",
            "psycopg2-binary", "sqlalchemy>=2.0", "eralchemy2",
        ],
    },
    scripts=["pt"],
    entry_points={
        "console_scripts": [
            "pt=pt_cli.main:main",
        ],
    },
)
