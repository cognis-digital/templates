# cognis-mcp (MCP server template, Python)

A Model Context Protocol (MCP) server built on the official
[`mcp`](https://github.com/modelcontextprotocol/python-sdk) Python SDK. It
exposes a couple of example tools over stdio so any MCP client (Claude Desktop,
Claude Code, your own host) can call them.

## Layout

```
mcp-server-python/
  pyproject.toml
  src/cognis_mcp/
    __init__.py
    __main__.py
    server.py             # tool + resource definitions
  tests/
    test_server.py
```

## Quick start

```bash
uv venv
uv pip install -e ".[dev]"
uv run cognis-mcp          # serves over stdio
```

## Wire it into a client

Add to your MCP client config (e.g. Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "cognis-mcp": {
      "command": "uv",
      "args": ["run", "cognis-mcp"],
      "cwd": "/absolute/path/to/mcp-server-python"
    }
  }
}
```

## Tools provided

- `add(a, b)` — return the sum of two numbers.
- `slugify(text)` — turn arbitrary text into a URL-safe slug.
- Resource `cognis://about` — static server metadata.

Replace these with your own tools in `server.py`.
