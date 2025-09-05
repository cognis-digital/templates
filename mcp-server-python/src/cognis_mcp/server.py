"""A Model Context Protocol server exposing example tools.

Built on the FastMCP convenience layer of the official ``mcp`` SDK. Tools are
regular typed functions; the SDK derives the JSON schema from the annotations.

The pure logic (``add``, ``slugify``) is kept importable so it can be unit
tested without a running event loop.
"""

from __future__ import annotations

import re

from mcp.server.fastmcp import FastMCP

from cognis_mcp import __version__

mcp = FastMCP("cognis-mcp")

_SLUG_STRIP = re.compile(r"[^a-z0-9]+")


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def slugify(text: str) -> str:
    """Turn arbitrary text into a URL-safe, lowercase, hyphenated slug."""
    slug = _SLUG_STRIP.sub("-", text.strip().lower())
    return slug.strip("-")


@mcp.tool()
def add_tool(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return add(a, b)


@mcp.tool()
def slugify_tool(text: str) -> str:
    """Convert text into a URL-safe slug."""
    return slugify(text)


@mcp.resource("cognis://about")
def about() -> str:
    """Static metadata describing this server."""
    return f"cognis-mcp v{__version__} - a Cognis Digital MCP server template."


def main() -> None:
    """Run the server over stdio."""
    mcp.run()
