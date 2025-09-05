# cognis-tool (Python CLI template)

A minimal, modern Python CLI scaffold. Subcommands via `argparse`, packaged as a
console entry point, fully typed, tested with `pytest`.

## Layout

```
python-cli/
  pyproject.toml          # project + tool config (ruff, mypy, pytest)
  src/cognis_tool/
    __init__.py
    __main__.py           # enables `python -m cognis_tool`
    cli.py                # argument parser + dispatch
    commands.py           # command implementations
  tests/
    test_cli.py
```

## Quick start

```bash
# with uv (preferred)
uv venv
uv pip install -e ".[dev]"
uv run cognis-tool greet --name World

# or plain pip
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
cognis-tool greet --name World
```

## Develop

```bash
ruff check . && ruff format --check .
mypy src
pytest
```

## Rename for your project

1. Rename `src/cognis_tool/` to your package name (import-safe, underscores).
2. Update `name`, `[project.scripts]`, and `[tool.*]` paths in `pyproject.toml`.
3. Replace this README.
