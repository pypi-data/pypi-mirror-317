"""Console entry point for CCFT-PyMarkdown."""

import functools
import subprocess
import sys
from argparse import ArgumentParser
from typing import TYPE_CHECKING

from ccft_pymarkdown import (
    clean_custom_formatted_tables,
    restore_files,
    utils,
)
from ccft_pymarkdown.context_manager import CleanCustomFormattedTables

if TYPE_CHECKING:
    from argparse import Namespace, _SubParsersAction
    from collections.abc import Sequence
    from subprocess import CompletedProcess
    from typing import Final

    type SubParserGroup = _SubParsersAction[ArgumentParser]

__all__: "Sequence[str]" = ("run",)


def _run_clean(arg_parser: ArgumentParser) -> int:
    clean_tables_file_exists_error: FileExistsError
    try:
        clean_custom_formatted_tables.clean_custom_formatted_tables_from_all_files()

    except FileExistsError as clean_tables_file_exists_error:
        MANUAL_CLEAN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS: Final[bool] = (
            bool(clean_tables_file_exists_error.args)
            and "already exists" in clean_tables_file_exists_error.args[0]
        )
        if MANUAL_CLEAN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS:
            MANUAL_CLEAN_TABLES_FILE_EXISTS_ERROR_MESSAGE: Final[str] = (
                f"{clean_tables_file_exists_error.args[0]} "
                f"Use `{arg_parser.prog} restore` to first restore the files "
                "to their original state."
            )
            raise type(clean_tables_file_exists_error)(
                MANUAL_CLEAN_TABLES_FILE_EXISTS_ERROR_MESSAGE
            ) from clean_tables_file_exists_error

        raise clean_tables_file_exists_error from clean_tables_file_exists_error

    return 0


def _run_restore() -> int:
    restore_files.restore_all_markdown_files()
    return 0


def _run_scan_all(arg_parser: ArgumentParser) -> int:
    clean_tables_file_exists_error: FileExistsError
    try:
        with CleanCustomFormattedTables():
            parser_output: CompletedProcess[bytes] = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pymarkdown",
                    "--return-code-scheme",
                    "minimal",
                    "scan",
                    utils.PROJECT_ROOT.resolve(),
                ],
                check=True,
            )

    except FileExistsError as clean_tables_file_exists_error:
        WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS: Final[bool] = (
            bool(clean_tables_file_exists_error.args)
            and "already exists" in clean_tables_file_exists_error.args[0]
        )
        if WITH_PYMARKDOWN_ERROR_IS_ORIGINAL_FILE_ALREADY_EXISTS:
            WITH_PYMARKDOWN_CLEAN_TABLES_FILE_EXISTS_ERROR_MESSAGE: Final[str] = (
                f"{clean_tables_file_exists_error.args[0]} "
                f"Use `{arg_parser.prog} restore` to first restore the files "
                "to their original state."
            )
            raise type(clean_tables_file_exists_error)(
                WITH_PYMARKDOWN_CLEAN_TABLES_FILE_EXISTS_ERROR_MESSAGE
            ) from clean_tables_file_exists_error

        raise clean_tables_file_exists_error from clean_tables_file_exists_error

    return parser_output.returncode


def _set_up_arg_parser() -> ArgumentParser:
    arg_parser: ArgumentParser = ArgumentParser(
        prog="ccft-pymarkdown",
        description="Lint Markdown files after removing custom-formatted tables.",
    )

    action_sub_parser_group: SubParserGroup = arg_parser.add_subparsers(
        title="action",
        required=True,
        dest="action",
    )

    clean_action_sub_parser: ArgumentParser = action_sub_parser_group.add_parser(
        "clean",
        help="Manually clean custom-formatted tables from all Markdown files.",
    )
    clean_action_sub_parser.set_defaults(
        run_func=functools.partial(_run_clean, arg_parser=arg_parser),
    )

    restore_action_sub_parser: ArgumentParser = action_sub_parser_group.add_parser(
        "restore",
        help="Manually restore custom formatted tables from all Markdown files.",
    )
    restore_action_sub_parser.set_defaults(run_func=_run_restore)

    scan_all_action_sub_parser: ArgumentParser = action_sub_parser_group.add_parser(
        "scan-all",
        help="Lint all Markdown files after removing custom-formatted tables.",
    )
    scan_all_action_sub_parser.set_defaults(
        run_func=functools.partial(_run_scan_all, arg_parser=arg_parser),
    )

    return arg_parser


def run(argv: "Sequence[str] | None" = None) -> int:
    """Run CCFT-PyMarkdown."""
    arg_parser: ArgumentParser = _set_up_arg_parser()

    parsed_args: Namespace = arg_parser.parse_args(argv)

    return_value: object = parsed_args.run_func()
    if not isinstance(return_value, int):
        INVALID_ACTION_RETURN_TYPE: Final[str] = (
            f"Action {parsed_args.action}'s run_func did not return an integer."
        )
        raise TypeError(INVALID_ACTION_RETURN_TYPE)

    return return_value
