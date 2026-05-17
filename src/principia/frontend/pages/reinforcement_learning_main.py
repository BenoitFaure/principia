"""Default reinforcement learning workspace."""

from __future__ import annotations

from nicegui import ui

from principia.frontend.components.base_layout import base_two_pane_layout
from principia.frontend.language import LearningStage, get_user_language
from principia.frontend.theme import apply_theme
from principia.services.translator import translator


def reinforcement_learning_main() -> None:
    """Render the reinforcement learning main window."""
    language = get_user_language()
    apply_theme()
    base_two_pane_layout(
        language,
        LearningStage.REINFORCEMENT,
        left_content=_empty_workspace,
        right_content=_constitution_workspace,
    )


def _empty_workspace(language: str) -> None:
    pass


def _constitution_workspace(language: str) -> None:
    ui.label(
        translator.translate(
            "reinforcement_learning_main.constitution_title",
            language,
        ),
    ).classes("principia-window-title")
    ui.element("ul").classes("principia-constitution-list")
