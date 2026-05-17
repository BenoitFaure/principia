"""Default supervised learning workspace."""

from __future__ import annotations

from nicegui import ui

from principia.frontend.components.base_layout import base_two_pane_layout
from principia.frontend.language import get_user_language
from principia.frontend.theme import apply_theme
from principia.services.translator import translator


def register_supervised_learning_main_page() -> None:
    """Register the default supervised learning window."""

    @ui.page("/")
    def supervised_learning_main() -> None:
        language = get_user_language()
        apply_theme()
        base_two_pane_layout(
            language,
            left_content=_empty_workspace,
            right_content=_constitution_workspace,
        )


def _empty_workspace(language: str) -> None:
    pass


def _constitution_workspace(language: str) -> None:
    ui.label(
        translator.translate("supervised_learning_main.constitution_title", language),
    ).classes("principia-window-title")
    ui.element("ul").classes("principia-constitution-list")
