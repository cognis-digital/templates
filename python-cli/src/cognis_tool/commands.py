"""Command implementations.

Each command takes the parsed ``argparse.Namespace`` and returns an exit code.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def greet(args: argparse.Namespace) -> int:
    """Print a greeting for ``args.name``."""
    name: str = args.name
    if not name.strip():
        print("error: --name must not be blank", file=sys.stderr)
        return 2
    message = f"Hello, {name}!"
    if args.shout:
        message = message.upper()
    print(message)
    return 0


def count(args: argparse.Namespace) -> int:
    """Count lines from a file path or stdin."""
    if args.path:
        path = Path(args.path)
        if not path.exists():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 2
        if not path.is_file():
            print(f"error: not a regular file: {path}", file=sys.stderr)
            return 2
        try:
            text = path.read_text(encoding="utf-8")
        except PermissionError as exc:
            print(f"error: permission denied reading {path}: {exc}", file=sys.stderr)
            return 2
        except UnicodeDecodeError as exc:
            print(f"error: file is not valid UTF-8: {path}: {exc}", file=sys.stderr)
            return 2
        except OSError as exc:
            print(f"error: could not read {path}: {exc}", file=sys.stderr)
            return 1
    else:
        try:
            text = sys.stdin.read()
        except OSError as exc:
            print(f"error: could not read stdin: {exc}", file=sys.stderr)
            return 1

    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    print(lines)
    return 0
