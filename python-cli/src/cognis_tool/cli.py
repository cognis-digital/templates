"""Command-line entry point and argument parsing."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from cognis_tool import __version__, commands


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="cognis-tool",
        description="A Cognis Digital command-line tool.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    sub = parser.add_subparsers(dest="command", required=True, metavar="<command>")

    greet = sub.add_parser("greet", help="Print a friendly greeting.")
    greet.add_argument("--name", default="World", help="Who to greet.")
    greet.add_argument(
        "--shout",
        action="store_true",
        help="Render the greeting in uppercase.",
    )
    greet.set_defaults(func=commands.greet)

    count = sub.add_parser("count", help="Count lines on stdin or in a file.")
    count.add_argument(
        "path",
        nargs="?",
        help="File to read. Reads stdin when omitted.",
    )
    count.set_defaults(func=commands.count)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and dispatch to the selected command.

    Returns a process exit code.  Unexpected errors are caught and printed to
    stderr so the caller always gets a clean non-zero exit rather than a raw
    traceback.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        print("", file=sys.stderr)  # newline after ^C
        return 130
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1
