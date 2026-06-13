"""pt — Python Tools unified CLI."""

import sys
from pathlib import Path

import click

# Ensure the project root is on sys.path so `import excel.cli` etc. works
_PROJECT_ROOT = str(Path(__file__).resolve().parent)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)


@click.group()
@click.version_option(version="0.1.0", prog_name="pt")
def cli():
    """pt — 可复用 Python 工具集

    统一入口，按模块调用子命令。
    使用 `pt <module> --help` 查看各模块用法。
    """
    pass


# ---------------------------------------------------------------------------
# Module registry — each module defines create_cli() returning a click.Group
# ---------------------------------------------------------------------------

_MODULE_DIRS = [
    "excel",
    "pdf",
    "api",
    "text",
    "encoding",
    "conversion",
    "db",
    "file",
    "media",
    "network",
]


def _discover_and_register():
    """Import each module's cli.create_cli() and attach as a sub-command."""
    import importlib
    import logging

    logger = logging.getLogger("pt_cli")

    for mod_name in _MODULE_DIRS:
        try:
            mod = importlib.import_module(f"{mod_name}.cli")
        except Exception:
            logger.debug("Skipping %s.cli (import failed)", mod_name)
            continue

        factory = getattr(mod, "create_cli", None)
        if factory is None:
            continue

        group = factory()
        if isinstance(group, click.BaseCommand):
            cli.add_command(group, name=mod_name)


# Auto-register all modules at import time
_discover_and_register()


def main():
    """Entry point for the pt CLI."""
    cli()


if __name__ == "__main__":
    main()
