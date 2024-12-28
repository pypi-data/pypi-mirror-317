"""Automated test suite for argument parsing within `console.py`."""

from typing import TYPE_CHECKING, Final

from ccft_pymarkdown import console

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Final

    from _pytest.capture import CaptureFixture, CaptureResult

__all__: "Sequence[str]" = ()


class TestConsoleRun:
    """Test case to unit-test the `run` function."""

    USAGE_MESSAGE: "Final[str]" = "usage: ccft-pymarkdown [-h] {clean,restore,scan-all}"

    def test_error_when_no_args(self, capsys: "CaptureFixture[str]") -> None:
        EXPECTED_ERROR_MESSAGE: Final[str] = (
            "error: the following arguments are required: action"
        )

        e: SystemExit
        try:
            return_code: int = console.run([])
        except SystemExit as e:
            return_code = 0 if not e.code else int(e.code)

        capture_result: CaptureResult[str] = capsys.readouterr()

        assert return_code != 0
        assert not capture_result.out
        assert self.USAGE_MESSAGE in capture_result.err
        assert EXPECTED_ERROR_MESSAGE in capture_result.err
