"""Reusable page shell for Principia's two-pane workspace."""

from __future__ import annotations

from collections.abc import Callable

from nicegui import ui

from principia.frontend.language import set_user_language
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
    with ui.element("div").classes("principia-toolbar-shell"):
        with ui.element("nav").classes("principia-toolbar"):
            ui.button(_translate("toolbar.settings", language)).classes(
                "principia-toolbar-button",
            ).props("flat")
            ui.button(_translate("toolbar.information", language)).classes(
                "principia-toolbar-button",
            ).props("flat")

            with (
                ui.button(_translate("toolbar.language", language))
                .classes(
                    "principia-toolbar-button principia-language-button",
                )
                .props("flat")
            ):
                with ui.menu().classes("principia-language-menu"):
                    with ui.scroll_area().classes("principia-language-scroll"):
                        for language_code in translator.available_languages():
                            ui.menu_item(
                                _translate(f"language.{language_code}", language),
                                on_click=_language_selector(language_code),
                            )

            ui.button(_translate("toolbar.supervised_learning", language)).classes(
                "principia-toolbar-button",
            ).props("flat")

        ui.element("div").classes("principia-toolbar-divider")


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
