"""Command implementations.

Each command takes the parsed ``argparse.Namespace`` and returns an exit code.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def greet(args: argparse.Namespace) -> int:
    """Print a greeting for ``args.name``."""
    message = f"Hello, {args.name}!"
    if args.shout:
        message = message.upper()
    print(message)
    return 0


def count(args: argparse.Namespace) -> int:
    """Count lines from a file path or stdin."""
    if args.path:
        path = Path(args.path)
        if not path.is_file():
            print(f"error: no such file: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
    else:
        text = sys.stdin.read()

    lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    print(lines)
    return 0
