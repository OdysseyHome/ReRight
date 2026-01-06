"""Sanitization helpers for filenames and folders.

This module provides simple helpers to sanitize file and folder names
to a portable ASCII-friendly format and functions to rename items on
disk (used with care).
"""

# --- IMPORTS ---

# --- First Party
import logging
import re
import unicodedata
from pathlib import Path
from typing import Annotated

# --- Third Party
import typer
from rich.logging import RichHandler

# --- CONFIG AND GLOBAL

app = typer.Typer()
log = logging.getLogger("sanitizer")

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],  # Makes logs look like a pro dev tool
)

# --- CORE UTILITIES ---


def sanitize_name(name: str) -> str:
    """Sanitize a filename or folder name.

    Converts to lowercase, removes accents, replaces spaces/special
    characters with hyphens, and cleans up extra hyphens.

    Args:
        name (str): The original filename or folder name

    Returns:
        str: The sanitized name

    """
    # 1. Decompose accents (e.g., 'ñ' becomes 'n' + '~')
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")

    # 2. Lowercase
    name = name.lower()

    # 3. Replace spaces and special chars with a hyphen
    # This regex keeps letters, numbers, and dots (for extensions)
    name = re.sub(r"[^a-z0-9.]+", "-", name)

    # 4. Clean up: collapse multiple hyphens and remove leading/trailing ones
    name = re.sub(r"-+", "-", name)
    name = name.strip("-")

    return name


def rename_item(item_path: Path, item_type: str, dry_run: bool) -> None:
    """Rename a single file or folder item.

    Args:
        item_path (Path): Path object to the item
        item_type (str): "FILE" or "FOLDER"
        dry_run (bool): If True, only print. If False, apply changes.

    """
    old_name = item_path.name
    new_name = sanitize_name(old_name)
    new_path = item_path.with_name(new_name)

    if item_path == new_path:
        return

    if new_path.exists():
        log.error(f"Naming Collision: {new_path} already exists. Skipping.")
        return

    if dry_run:
        log.info(f"[DRY RUN] {item_type}: {old_name} -> {new_name}")
    else:
        try:
            item_path.rename(new_path)
            log.info(f"[SUCCESS: {old_name} -> {new_name}")
        except PermissionError:
            log.error(f"[{item_type}] Permission denied renaming {old_name}")
        except Exception as e:
            log.error(f"UNEXPECTED ERROR: {e}")


def rename_files(target_path: Path, dry_run: bool = True) -> None:
    """Recursively sanitize all filenames and folder names in a directory.

    Processes nested items first (topdown=False) to ensure folders are
    renamed after their contents.

    Args:
        target_path (str): Path to the vault directory
        dry_run (bool): If True, only print changes. If False, apply them.
                       Default is True for safety.

    Returns:
        None

    """
    if not target_path.exists():
        logging.error(f"Error: Path does not exist: {target_path}")
        return

    # Gather everything
    paths = list(target_path.rglob("*"))

    # Sort by depth (deepest first) to avoid `Path Not Found` errors
    paths.sort(key=lambda p: len(p.parts), reverse=True)

    logging.info(f"Found {len(paths)} items to sanitize")

    # Wrap the loop in a progress bar
    with typer.progressbar(paths, label="Sanitizing...") as progress:
        for p in progress:
            kind = "FOLDER" if p.is_dir() else "FILE"
            rename_item(p, kind, dry_run)


# --- CLI COMMANDS ---


@app.command()
def run_sanitizer(
    path: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="Target directory path to sanitize",
        ),
    ],
    apply: Annotated[
        bool,
        typer.Option(
            "--apply", "-a", help="Apply changes (disable the default dry-run)"
        ),
    ] = False,
) -> None:
    """Recursively sanitize filenames and folders to ASCII."""
    dry_run = not apply

    log.info(f"Scanning: {path}")
    if dry_run:
        typer.secho("\n--- DRY RUN MODE ---", fg=typer.colors.YELLOW, bold=True)
        typer.secho(
            "No files will be changed. Use --apply to execute.\n", fg=typer.colors.CYAN
        )
    else:
        typer.secho("\n!!! LIVE MODE !!!", fg=typer.colors.RED, bold=True, blink=True)

    rename_files(path, dry_run=dry_run)


# --- ENTRY POINT ---


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    app()
