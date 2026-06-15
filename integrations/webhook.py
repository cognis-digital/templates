#!/usr/bin/env python3
"""Minimal, dependency-free webhook forwarder for Cognis findings.

Reads JSON findings on stdin and POSTs them to a URL (SIEM/Slack/Jira bridge).
Usage:  <tool> scan . --format json | python integrations/webhook.py --url URL
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from urllib.parse import urlparse


def _validate_url(url: str) -> str:
    """Validate that *url* is an absolute http/https URL."""
    try:
        parsed = urlparse(url)
    except Exception as exc:
        raise ValueError(f"unparseable URL: {exc}") from exc
    if parsed.scheme not in {"http", "https"}:
        raise ValueError(f"URL must start with http:// or https://, got: {url!r}")
    if not parsed.netloc:
        raise ValueError(f"URL has no host: {url!r}")
    return url


def _parse_header(raw: str) -> tuple[str, str]:
    """Split a 'Name: Value' header string; raise ValueError on bad format."""
    if ":" not in raw:
        raise ValueError(
            f"--header must be in 'Name: Value' format, got: {raw!r}"
        )
    name, _, value = raw.partition(":")
    name = name.strip()
    if not name:
        raise ValueError(f"--header has an empty name in: {raw!r}")
    return name, value.strip()


def main() -> int:
    ap = argparse.ArgumentParser(
        description="POST JSON findings to a webhook URL."
    )
    ap.add_argument("--url", required=True, help="Destination http/https URL.")
    ap.add_argument(
        "--header",
        action="append",
        default=[],
        help="Extra request header in 'Name: Value' format (repeatable).",
    )
    args = ap.parse_args()

    # Validate URL early so the error is clear before we read stdin.
    try:
        url = _validate_url(args.url)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    # Parse and validate all headers before touching stdin.
    headers: list[tuple[str, str]] = []
    for raw in args.header:
        try:
            headers.append(_parse_header(raw))
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    # Read stdin and verify it is valid JSON before sending.
    try:
        raw_stdin = sys.stdin.read()
    except OSError as exc:
        print(f"error reading stdin: {exc}", file=sys.stderr)
        return 1

    if not raw_stdin.strip():
        print("error: stdin is empty — nothing to post", file=sys.stderr)
        return 2

    try:
        json.loads(raw_stdin)
    except json.JSONDecodeError as exc:
        print(f"error: stdin is not valid JSON: {exc}", file=sys.stderr)
        return 2

    payload = raw_stdin.encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    for name, value in headers:
        req.add_header(name, value)

    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"posted {len(payload)} bytes -> {r.status}")
        return 0
    except OSError as exc:
        print(f"webhook error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
