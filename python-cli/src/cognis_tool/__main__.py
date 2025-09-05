"""Enable `python -m cognis_tool`."""

from __future__ import annotations

import sys

from cognis_tool.cli import main

if __name__ == "__main__":
    sys.exit(main())
