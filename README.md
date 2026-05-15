# Principia
An interface to generate a Constitution to be used in Supervised Learning and Reinforcement Learning. Alongside generating the datasets for them. Based on Constitutional AI paper by Antropic.

## Installation
 
### Option 1 — Dev container (recommended)
 
The dev container sets up the full environment automatically, including Python, uv, and all dependencies. It's like magic!
 
**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) and the [Dev Containers VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
 
```bash
git clone https://github.com/yourname/principia.git
cd principia
code .
```
 
When VS Code opens, click **Reopen in Container** when prompted (or open the command palette with `Ctrl+Shift+P` and select `Dev Containers: Reopen in Container`).
 
The container will install all dependencies automatically via `uv sync`. This may take a minute on first build.
 
---
 
### Option 2 — uv
 
**Prerequisites:** [uv](https://docs.astral.sh/uv/getting-started/installation/) installed on your machine.
 
```bash
git clone https://github.com/yourname/principia.git
cd principia
uv sync --all-groups
```
 
---
 
### Option 3 — pip
 
**Prerequisites:** Python 3.12 or higher.
 
```bash
git clone https://github.com/yourname/principia.git
cd principia
pip install . -e
```
 
To also install dev and docs dependencies:
 
```bash
pip install ".[dev,docs]"
```
 
---
 
## Usage
 
### Running the app
 
```bash
# With uv
uv run principia
 
# With pip install
principia
```
 
This starts Principia and opens it in your browser at `http://localhost:8080`.
 
---

### Linting and formatting
 
Principia uses [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting.
 
```bash
# Check for lint errors
uv run ruff check .
 
# Fix lint errors automatically
uv run ruff check . --fix
 
# Format code
uv run ruff format .
 
# Check formatting without writing changes
uv run ruff format . --check
```
 
---
 
### Type checking
 
```bash
uv run pyright
```
 
---
 
### Running tests
 
```bash
# Run all tests
uv run pytest
```
 
---
 
### Building the documentation
 
```bash
# Install docs dependencies first (if using uv)
uv sync --group docs
 
# Build HTML docs
uv run sphinx-build docs docs/_build/html
 
# Serve docs locally
uv run python -m http.server 8081 --directory docs/_build/html
```
 
Then open `http://localhost:8081` in your browser.