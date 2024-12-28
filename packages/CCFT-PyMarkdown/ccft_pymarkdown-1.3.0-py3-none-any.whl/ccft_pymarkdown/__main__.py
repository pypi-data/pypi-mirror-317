"""Command-line execution of the `ccft_pymarkdown` package."""

from typing import TYPE_CHECKING

from ccft_pymarkdown import console

if TYPE_CHECKING:
    from collections.abc import Sequence

__all__: "Sequence[str]" = ()

if __name__ == "__main__":
    raise SystemExit(console.run())
