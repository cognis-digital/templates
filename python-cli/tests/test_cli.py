"""Tests for the CLI."""

from __future__ import annotations

import io

import pytest

from cognis_tool.cli import main


def test_greet_default(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["greet"]) == 0
    assert capsys.readouterr().out.strip() == "Hello, World!"


def test_greet_named_and_shout(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["greet", "--name", "Cognis", "--shout"]) == 0
    assert capsys.readouterr().out.strip() == "HELLO, COGNIS!"


def test_count_stdin(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO("a\nb\nc\n"))
    assert main(["count"]) == 0
    assert capsys.readouterr().out.strip() == "3"


def test_count_missing_file(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["count", "does-not-exist.txt"]) == 2
    assert "no such file" in capsys.readouterr().err


def test_requires_subcommand() -> None:
    with pytest.raises(SystemExit):
        main([])


# ---------------------------------------------------------------------------
# Hardening tests — error paths and edge cases
# ---------------------------------------------------------------------------

def test_greet_blank_name(capsys: pytest.CaptureFixture[str]) -> None:
    """Blank --name should return exit-2 with a message on stderr."""
    assert main(["greet", "--name", "   "]) == 2
    assert "blank" in capsys.readouterr().err


def test_count_empty_stdin(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An empty stdin should count as 0 lines (not crash)."""
    monkeypatch.setattr("sys.stdin", io.StringIO(""))
    assert main(["count"]) == 0
    assert capsys.readouterr().out.strip() == "0"


def test_count_file_no_trailing_newline(
    tmp_path: pytest.TempPathFactory, capsys: pytest.CaptureFixture[str]
) -> None:
    """A file with no trailing newline still counts its single line."""
    f = tmp_path / "no_newline.txt"
    f.write_text("hello", encoding="utf-8")
    assert main(["count", str(f)]) == 0
    assert capsys.readouterr().out.strip() == "1"


def test_count_directory_returns_error(
    tmp_path: pytest.TempPathFactory, capsys: pytest.CaptureFixture[str]
) -> None:
    """Passing a directory path should return exit-2 with an error message."""
    result = main(["count", str(tmp_path)])
    assert result == 2
    assert capsys.readouterr().err != ""


def test_count_binary_file_returns_error(
    tmp_path: pytest.TempPathFactory, capsys: pytest.CaptureFixture[str]
) -> None:
    """A non-UTF-8 binary file should return exit-2 with a clear error."""
    f = tmp_path / "binary.bin"
    f.write_bytes(bytes(range(256)))
    result = main(["count", str(f)])
    assert result == 2
    assert "UTF-8" in capsys.readouterr().err


def test_unexpected_command_error_returns_1(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """An unexpected exception in a command should be caught; exit code 1."""
    from cognis_tool import commands

    def _boom(args: object) -> int:
        raise RuntimeError("simulated internal failure")

    monkeypatch.setattr(commands, "greet", _boom)
    result = main(["greet"])
    assert result == 1
    err = capsys.readouterr().err
    assert "simulated internal failure" in err
