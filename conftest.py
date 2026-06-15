"""Root conftest.py — makes sub-project src/ trees importable from a root pytest run.

Each sub-project has ``pythonpath = ["src"]`` in its own pyproject.toml, but
pytest only applies that setting when invoked from the sub-project directory.
Running ``pytest`` from the repo root skips those settings, causing
ModuleNotFoundError for ``cognis_tool`` and ``cognis_mcp``.

This file inserts each ``<subproject>/src`` directory into ``sys.path`` so that
``python -m pytest`` (or plain ``pytest``) from the repo root works on a fresh
clone without requiring ``pip install -e .`` first.
"""
from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).parent

for _src in _REPO_ROOT.glob("*/src"):
    _s = str(_src)
    if _s not in sys.path:
        sys.path.insert(0, _s)

# Also make the integrations/ directory importable so webhook tests can use
# `import webhook` without requiring an install step.
_integrations = str(_REPO_ROOT / "integrations")
if _integrations not in sys.path:
    sys.path.insert(0, _integrations)
