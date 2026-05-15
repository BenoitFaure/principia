# .devcontainer/setup.sh
#!/bin/bash
set -e

if [ ! -f pyproject.toml ]; then
  echo "pyproject.toml not found — skipping uv sync"
  exit 0
fi

uv sync --all-groups