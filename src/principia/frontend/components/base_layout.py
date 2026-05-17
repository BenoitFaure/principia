"""Reusable page shell for Principia's two-pane workspace."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from nicegui import ui

from principia.frontend.language import (
    UserSettings,
    get_user_settings,
    save_user_settings,
    set_user_language,
)
from principia.services.translator import translator

PaneBuilder = Callable[[str], None]


def base_two_pane_layout(
    language: str,
    left_content: PaneBuilder | None = None,
    right_content: PaneBuilder | None = None,
) -> None:
    """Render the shared screen-sized two-pane layout."""
    with ui.element("main").classes("principia-screen"):
        with ui.element("div").classes("principia-shell"):
            with ui.element("section").classes(
                "principia-pane principia-pane-left",
            ):
                _toolbar(language)
                _pane_content(language, left_content, "home.left.placeholder")

            ui.element("div").classes("principia-vertical-separator")

            with ui.element("section").classes(
                "principia-pane principia-pane-right",
            ):
                _pane_content(language, right_content, "home.right.placeholder")


def _toolbar(language: str) -> None:
    settings_dialog = _settings_dialog(language)

    with ui.element("div").classes("principia-toolbar-shell"):
        with ui.element("nav").classes("principia-toolbar"):
            ui.button(
                _translate("toolbar.settings", language),
                on_click=settings_dialog.open,
            ).classes("principia-toolbar-button").props("flat")
            ui.button(_translate("toolbar.information", language)).classes(
                "principia-toolbar-button",
            ).props("flat")

            with (
                ui.button(_language_label(language))
                .classes(
                    "principia-toolbar-button principia-language-button",
                )
                .props("flat")
            ):
                with ui.menu().classes("principia-language-menu"):
                    with ui.scroll_area().classes("principia-language-scroll"):
                        for language_code in translator.available_languages():
                            ui.menu_item(
                                _language_label(language_code),
                                on_click=_language_selector(language_code),
                            )

            ui.button(_translate("toolbar.supervised_learning", language)).classes(
                "principia-toolbar-button",
            ).props("flat")

        ui.element("div").classes("principia-toolbar-divider")


def _settings_dialog(language: str) -> Any:
    settings = get_user_settings()
    language_options = {
        language_code: _language_label(language_code)
        for language_code in translator.available_languages()
    }

    with ui.dialog().classes("principia-settings-dialog") as dialog:
        with ui.card().classes("principia-settings-card"):
            ui.label(_translate("settings.title", language)).classes(
                "principia-settings-title",
            )
            language_select = ui.select(
                language_options,
                value=settings.language,
                label=_translate("settings.language", language),
            ).classes("principia-settings-control")
            api_key_input = ui.input(
                label=_translate("settings.openai_api_key", language),
                value=settings.openai_api_key,
                password=True,
                password_toggle_button=True,
            ).classes("principia-settings-control")

            with ui.row().classes("principia-settings-actions"):
                ui.button(
                    _translate("settings.cancel", language),
                    on_click=dialog.close,
                ).classes("principia-settings-button").props("flat")
                ui.button(
                    _translate("settings.save", language),
                    on_click=lambda: _save_settings(
                        dialog,
                        str(language_select.value),
                        str(api_key_input.value or ""),
                    ),
                ).classes("principia-settings-button principia-settings-save").props(
                    "flat",
                )

    return dialog


def _save_settings(dialog: Any, language: str, openai_api_key: str) -> None:
    previous_language = get_user_settings().language
    save_user_settings(UserSettings(language=language, openai_api_key=openai_api_key))
    dialog.close()
    if language != previous_language:
        ui.run_javascript("window.location.reload()")


def _pane_content(
    language: str,
    content: PaneBuilder | None,
    placeholder_key: str,
) -> None:
    with ui.element("div").classes("principia-pane-content"):
        if content is None:
            ui.label(_translate(placeholder_key, language)).classes(
                "principia-placeholder",
            )
            return

        content(language)


def _language_selector(language: str) -> Callable[[], None]:
    def select_language() -> None:
        set_user_language(language)
        ui.run_javascript("window.location.reload()")

    return select_language


def _translate(element: str, language: str) -> str:
    return translator.translate(element, language)


def _language_label(language: str) -> str:
    return language.upper()
