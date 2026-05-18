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
        left_content=_upcoming_feature_workspace,
    )


def _upcoming_feature_workspace(language: str) -> None:
    with ui.element("div").classes("principia-placeholder"):
        ui.label(
            translator.translate(
                "reinforcement_learning_main.upcoming_feature",
                language,
            ),
        ).classes("principia-window-title")
