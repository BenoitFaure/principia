# AGENTS.md

## Project Shape
- Python 3.12 `uv` project using a `src/` layout; install/sync with `uv sync --all-groups`.
- The console script is `principia = principia.main:main`; `uv run principia` starts NiceGUI and opens `http://localhost:8080`.
- `src/principia/main.py` includes the FastAPI router from `principia.backend.api` under `/api` before calling `ui.run()`.
- API routes are rooted at `src/principia/backend/api/router.py`; `src/principia/backend/api/__init__.py` exports `router`.
- `frontend/components` and `frontend/pages` currently only contain package placeholders; do not assume an existing page/component framework beyond NiceGUI.

## Commands
- Setup: `uv sync --all-groups`.
- Run app: `uv run principia`.
- Lint: `uv run ruff check .`; auto-fix with `uv run ruff check . --fix`.
- Format: `uv run ruff format .`; check only with `uv run ruff format . --check`.
- Typecheck: `uv run pyright` (`pyproject.toml` includes only `src`).
- Tests: `uv run pytest`; focused tests use normal pytest selectors such as `uv run pytest tests/path.py::test_name`.
- Docs: `uv run sphinx-build docs docs/_build/html`; docs deps are in the `docs` group if not already synced.

## Repo-Specific Gotchas
- `pytest` is configured with `testpaths = ["tests"]`, but the repo currently has no `tests/` directory; add tests there.
- Ruff linting only selects `E`, `F`, `I`, and `UP`; do not infer stricter style rules from defaults.
- NiceGUI storage uses `NICEGUI_SECRET` if set, otherwise the default string `PRINCIPIA_SECRET` in local runs.
- Dev containers run `.devcontainer/setup.sh`, which only executes `uv sync --all-groups` when `pyproject.toml` exists.
- Sphinx imports project code by prepending `../src` in `docs/conf.py`; keep generated docs in `docs/_build/` out of source edits.
