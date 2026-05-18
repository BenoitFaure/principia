"""OpenAI model list parsed from model_list.md."""

from __future__ import annotations

from pathlib import Path

_MODEL_LIST_PATH = Path(__file__).parent / "model_list.md"

DEFAULT_MODEL = "gpt-4o"


def _parse_models() -> list[str]:
    models = []
    for line in _MODEL_LIST_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            models.append(stripped[2:].strip())
    return models


AVAILABLE_MODELS: list[str] = _parse_models()
