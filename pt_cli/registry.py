"""Auto-discover and register sub-command groups from each module's cli.py."""

import importlib
import logging
from pathlib import Path

import click

logger = logging.getLogger("pt_cli.registry")

# Modules that provide a `cli` submodule with a `create_cli()` -> click.Group
MODULE_DIRS = [
    "excel",
    "pdf",
    "api",
    "text",
    "encoding",
    "conversion",
    "db",
    "file",
    "media",
]


def _project_root() -> Path:
    """Return the python-tools project root (parent of pt_cli/)."""
    return Path(__file__).resolve().parent.parent


def discover_commands() -> list[click.Group]:
    """Scan known module dirs and import their cli.create_cli() if present.

    Returns a list of click.Group objects ready to be added to the main CLI.
    """
    groups: list[click.Group] = []
    root = _project_root()

    for mod_name in MODULE_DIRS:
        mod_dir = root / mod_name
        cli_file = mod_dir / "cli.py"
        if not cli_file.is_file():
            continue

        try:
            mod = importlib.import_module(f"{mod_name}.cli")
            factory = getattr(mod, "create_cli", None)
            if factory is None:
                logger.debug("Skipping %s.cli — no create_cli()", mod_name)
                continue
            group = factory()
            if not isinstance(group, click.BaseCommand):
                logger.warning("%s.cli.create_cli() did not return a click command", mod_name)
                continue
            groups.append(group)
        except Exception:
            logger.warning("Failed to import %s.cli", mod_name, exc_info=True)

    return groups
