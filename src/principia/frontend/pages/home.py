"""Home page for the initial Principia workspace."""

from __future__ import annotations

from nicegui import ui

from principia.frontend.components.base_layout import base_two_pane_layout
from principia.frontend.language import LearningStage, get_user_language
from principia.frontend.theme import apply_theme


def register_home_page() -> None:
    """Register the root NiceGUI page."""

    @ui.page("/")
    def home_page() -> None:
        language = get_user_language()
        apply_theme()
        base_two_pane_layout(language, LearningStage.SUPERVISED)
