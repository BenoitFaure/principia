# .devcontainer/Dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Added libatomic1 to the system utilities setup
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspaces/principia

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    VIRTUAL_ENV=/workspaces/principia/.venv \
    PATH="/workspaces/principia/.venv/bin:$PATH"