"""Default supervised learning workspace."""

from __future__ import annotations

from nicegui import ui

from principia.backend.database import ConstitutionElement, ConstitutionFile
from principia.frontend.components.base_layout import base_two_pane_layout
from principia.frontend.components.supervised_learning_constitution_edit import (
    supervised_learning_constitution_edit,
)
from principia.frontend.language import LearningStage, get_user_language
from principia.frontend.theme import apply_theme
from principia.services.translator import translator


def supervised_learning_main() -> None:
    """Render the supervised learning main window."""
    language = get_user_language()
    apply_theme()
    base_two_pane_layout(
        language,
        LearningStage.SUPERVISED,
        left_content=_empty_workspace,
        right_content=_constitution_workspace,
    )


def _empty_workspace(language: str) -> None:
    with ui.element("div").classes("principia-placeholder"):
        ui.label(
            translator.translate("home.left.placeholder", language),
        ).classes("principia-window-title")


def _constitution_workspace(language: str) -> None:
    ui.button(
        translator.translate("supervised_learning_main.constitution_title", language),
        on_click=lambda: ui.run_javascript(
            "window.location.href = '/supervised/constitution/edit'",
        ),
    ).classes("principia-window-title principia-window-title-button").props(
        "flat no-caps",
    )
    with ui.element("div").classes("principia-constitution-stack"):
        for element in ConstitutionFile().read():
            _constitution_widget(language, element)

        create_dialog = supervised_learning_constitution_edit(language, None)
        ui.button("+", on_click=create_dialog.open).classes(
            "principia-constitution-add",
        ).props("flat")


def _constitution_widget(language: str, element: ConstitutionElement) -> None:
    edit_dialog = supervised_learning_constitution_edit(language, element)
    preview = element.critique_prompt or translator.translate(
        "supervised_learning_main.empty_critique_prompt",
        language,
    )

    with (
        ui.button(on_click=edit_dialog.open)
        .classes(
            "principia-constitution-widget",
        )
        .props("flat no-caps")
    ):
        ui.label(preview).classes("principia-constitution-critique")
