"""Suppress custom-formatted table errors from PyMarkdown in Markdown files."""

from typing import TYPE_CHECKING

from ccft_pymarkdown.clean_custom_formatted_tables import (
    clean_custom_formatted_tables_from_all_files,
    clean_custom_formatted_tables_from_single_file,
)
from ccft_pymarkdown.console import run
from ccft_pymarkdown.context_manager import CleanCustomFormattedTables
from ccft_pymarkdown.restore_files import (
    restore_all_markdown_files,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__: "Sequence[str]" = (
    "CleanCustomFormattedTables",
    "clean_custom_formatted_tables_from_all_files",
    "clean_custom_formatted_tables_from_single_file",
    "restore_all_markdown_files",
    "run",
)
