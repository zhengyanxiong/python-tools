"""Optional dependency checking — warn at runtime instead of failing at import.

Usage in a module's cli.py:

    from common.deps import require

    require("openpyxl", "excel", hint="pip install -r requirements/excel.txt")
"""

import importlib
import sys


def require(package: str, module: str, *, hint: str = "") -> None:
    """Check that *package* is importable; exit with a helpful message if not.

    Args:
        package: The Python package name to import (e.g. "openpyxl").
        module:  The pt sub-command that needs it (e.g. "excel").
        hint:    Optional install hint (e.g. "pip install -r requirements/excel.txt").
    """
    try:
        importlib.import_module(package)
    except ImportError:
        hint = hint or f"pip install {package}"
        print(
            f"❌ 模块 '{module}' 需要依赖 '{package}'，请先安装：\n"
            f"   {hint}",
            file=sys.stderr,
        )
        sys.exit(1)


def is_available(package: str) -> bool:
    """Return True if *package* can be imported, False otherwise."""
    try:
        importlib.import_module(package)
        return True
    except ImportError:
        return False
