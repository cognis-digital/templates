# <Project Name>

> One-sentence description of what this project does and who it is for.

[![CI](https://github.com/cognis-digital/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/cognis-digital/<repo>/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

## Features

- Bullet the two or three things this project does well.
- Keep it concrete, not aspirational.

## Install

```bash
# with uv (preferred)
uv pip install <package-name>

# or pip
pip install <package-name>
```

## Usage

```bash
<command> --help
```

Show a real, copy-pasteable example and its output:

```bash
$ <command> greet --name World
Hello, World!
```

## Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `EXAMPLE_VAR` | `unset` | What this controls. |

## Development

```bash
git clone https://github.com/cognis-digital/<repo>.git
cd <repo>
uv venv && uv pip install -e ".[dev]"

ruff check . && mypy src && pytest
```

## Contributing

Issues and pull requests are welcome. Please read the PR checklist in
`.github/PULL_REQUEST_TEMPLATE.md` before opening a change.

## License

MIT (c) Cognis Digital. See [LICENSE](LICENSE).
