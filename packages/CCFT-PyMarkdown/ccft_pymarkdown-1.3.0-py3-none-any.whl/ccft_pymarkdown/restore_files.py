"""Perform the restoration of Markdown files that had custom-formatted tables cleaned."""

from typing import TYPE_CHECKING

from ccft_pymarkdown import utils

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

__all__: "Sequence[str]" = ("restore_all_markdown_files",)


def restore_all_markdown_files() -> None:
    """Return all Markdown files to their original state before cleaning."""
    file_path: Path
    for file_path in utils.PROJECT_ROOT.rglob("*.md.original"):
        FILE_IS_TEMPORARY_ORIGINAL: bool = (
            len(file_path.suffixes) == 2
            and file_path.suffixes[0] == ".md"
            and file_path.suffixes[1] == ".original"
        )
        if not FILE_IS_TEMPORARY_ORIGINAL:
            continue

        if not file_path.is_file() or not file_path.exists():
            continue

        correct_original_file_path: Path = file_path.parent / file_path.stem
        if correct_original_file_path.exists():
            correct_original_file_path.unlink()

        file_path.rename(file_path.parent / file_path.stem)
