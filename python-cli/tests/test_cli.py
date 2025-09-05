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
