"""Tests for the MCP server's pure logic.

The transport layer is exercised by the SDK; here we test the underlying
functions directly so the suite stays fast and deterministic.
"""

from __future__ import annotations

import pytest

from cognis_mcp.server import add, slugify


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [(1, 2, 3), (-1, 1, 0), (2.5, 0.5, 3.0)],
)
def test_add(a: float, b: float, expected: float) -> None:
    assert add(a, b) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Hello, World!", "hello-world"),
        ("  Cognis  Digital  ", "cognis-digital"),
        ("already-a-slug", "already-a-slug"),
        ("!!!", ""),
    ],
)
def test_slugify(text: str, expected: str) -> None:
    assert slugify(text) == expected
