"""Supervised learning page for testing one constitution critique."""

from __future__ import annotations

import json
from collections.abc import Callable

from nicegui import ui

from principia.backend.database import (
    ConstitutionElement,
    ConstitutionFile,
    DevElement,
    DevFile,
    ExampleElement,
    ExamplesFile,
)
from principia.frontend.components.base_layout import base_two_pane_layout
from principia.frontend.language import LearningStage, get_user_language
from principia.frontend.theme import apply_theme
from principia.services.translator import translator


def supervised_learning_constitution_test_page(constitution_hash: str) -> None:
    """Render the supervised learning test page for one constitution element."""
    language = get_user_language()
    apply_theme()

    constitutions = ConstitutionFile().read()
    constitution = next(
        (
            element
            for element in constitutions
            if element.constitution_hash == constitution_hash
        ),
        None,
    )
    examples = ExamplesFile().read()
    dev_prompts = DevFile().read()
    example_hashes = {example.example_hash for example in examples}
    selected_example_hashes = (
        set(constitution.example_hashes) if constitution is not None else set()
    )
    red_team_prompt: str | None = None

    def selected_hashes_in_example_order() -> list[str]:
        ordered_hashes = [
            example.example_hash
            for example in examples
            if example.example_hash in selected_example_hashes
        ]
        stale_hashes = sorted(selected_example_hashes - example_hashes)
        return ordered_hashes + stale_hashes

    def linked_examples() -> list[ExampleElement]:
        if constitution is None:
            return []
        linked_hashes = set(constitution.example_hashes)
        return [
            example for example in examples if example.example_hash in linked_hashes
        ]

    def toggle_example(example: ExampleElement) -> None:
        if example.example_hash in selected_example_hashes:
            selected_example_hashes.remove(example.example_hash)
        else:
            selected_example_hashes.add(example.example_hash)

        critique_workspace.refresh(language)

    def select_red_team_prompt(prompt: DevElement, dialog) -> None:
        nonlocal red_team_prompt
        red_team_prompt = prompt.user
        dialog.close()
        red_team_workspace.refresh(language)

    @ui.refreshable
    def critique_workspace(language: str) -> None:
        if constitution is None:
            ui.label(
                translator.translate("constitution_test.not_found", language),
            ).classes("principia-window-title")
            return

        with ui.element("div").classes("principia-test-stack"):
            _constitution_test_widget(
                language, constitution, selected_hashes_in_example_order
            )
            for example in linked_examples():
                _example_test_widget(
                    language,
                    example,
                    example.example_hash in selected_example_hashes,
                    toggle_example,
                )

    @ui.refreshable
    def red_team_workspace(language: str) -> None:
        ui.button(
            translator.translate("constitution_test.constitution_navigation", language),
            on_click=lambda: ui.run_javascript(
                "window.location.href = '/supervised/constitution/edit'",
            ),
        ).classes(
            "principia-edit-navigation-title principia-edit-navigation-title-enabled"
        ).props(
            "flat no-caps",
        )
        _red_team_prompt_widget(
            language,
            red_team_prompt,
            dev_prompts,
            select_red_team_prompt,
        )

    base_two_pane_layout(
        language,
        LearningStage.SUPERVISED,
        left_content=critique_workspace,
        right_content=red_team_workspace,
        stage_button_href="/",
    )


def _constitution_test_widget(
    language: str,
    constitution: ConstitutionElement,
    selected_hashes: Callable[[], list[str]],
) -> None:
    preview = constitution.critique_prompt or translator.translate(
        "supervised_learning_main.empty_critique_prompt",
        language,
    )

    with ui.row().classes("principia-link-row"):
        ui.button(
            "💾",
            on_click=lambda: _save_constitution(constitution, selected_hashes()),
        ).classes("principia-link-marker principia-test-save-marker").props(
            "flat no-caps",
        )
        with ui.element("div").classes("principia-constitution-widget"):
            ui.label(preview).classes("principia-constitution-critique")


def _example_test_widget(
    language: str,
    example: ExampleElement,
    selected: bool,
    on_marker_click,
) -> None:
    preview = example.user or translator.translate(
        "constitution_link.empty_user_prompt",
        language,
    )
    marker = "●" if selected else "○"
    marker_class = " principia-link-marker-selected" if selected else ""
    widget_class = " principia-link-widget-selected" if selected else ""

    with ui.row().classes("principia-link-row"):
        ui.button(
            marker,
            on_click=lambda: on_marker_click(example),
        ).classes(f"principia-link-marker{marker_class}").props("flat")
        with ui.element("div").classes(f"principia-example-widget{widget_class}"):
            with ui.element("div").classes("principia-example-content"):
                ui.label(preview).classes("principia-example-user")
                ui.label(example.example_hash).classes("principia-example-hash")


def _red_team_prompt_widget(
    language: str,
    selected_prompt: str | None,
    dev_prompts: list[DevElement],
    on_prompt_click,
) -> None:
    dialog = _red_team_prompt_dialog(language, dev_prompts, on_prompt_click)
    preview = selected_prompt or translator.translate(
        "constitution_test.red_team_prompt",
        language,
    )

    with (
        ui.button(on_click=dialog.open)
        .classes("principia-red-team-widget")
        .props("flat no-caps")
    ):
        ui.label(preview).classes("principia-red-team-preview")


def _red_team_prompt_dialog(
    language: str,
    dev_prompts: list[DevElement],
    on_prompt_click,
):
    previewed_prompt = dev_prompts[0] if dev_prompts else None

    def preview_or_select_prompt(prompt: DevElement, dialog) -> None:
        nonlocal previewed_prompt
        if prompt == previewed_prompt:
            on_prompt_click(prompt, dialog)
            return

        previewed_prompt = prompt
        red_team_dialog_content.refresh(language, dialog)

    def select_previewed_prompt(dialog) -> None:
        if previewed_prompt is None:
            return

        on_prompt_click(previewed_prompt, dialog)

    @ui.refreshable
    def red_team_dialog_content(language: str, dialog) -> None:
        ui.label(
            translator.translate("constitution_test.red_team_prompt", language),
        ).classes("principia-red-team-title")
        with ui.element("div").classes("principia-red-team-selector"):
            with ui.element("div").classes("principia-red-team-list"):
                for prompt in dev_prompts:
                    _dev_prompt_widget(
                        language,
                        prompt,
                        prompt == previewed_prompt,
                        dialog,
                        preview_or_select_prompt,
                    )
            _dev_prompt_chat(
                language,
                previewed_prompt,
                dialog,
                select_previewed_prompt,
            )

    with ui.dialog().classes("principia-red-team-dialog") as dialog:
        with ui.card().classes("principia-red-team-card"):
            red_team_dialog_content(language, dialog)

    return dialog


def _dev_prompt_widget(
    language: str,
    prompt: DevElement,
    previewed: bool,
    dialog,
    on_prompt_click,
) -> None:
    preview = prompt.user or translator.translate(
        "constitution_link.empty_user_prompt",
        language,
    )

    with (
        ui.button(on_click=lambda: on_prompt_click(prompt, dialog))
        .classes(
            "principia-dev-prompt-widget"
            f" {'principia-dev-prompt-widget-selected' if previewed else ''}",
        )
        .props("flat no-caps")
    ):
        ui.label(preview).classes("principia-dev-prompt-user")


def _dev_prompt_chat(
    language: str,
    prompt: DevElement | None,
    dialog,
    on_select_click,
) -> None:
    with ui.element("div").classes("principia-red-team-chat"):
        with ui.element("div").classes("principia-red-team-chat-messages"):
            if prompt is None:
                ui.label(
                    translator.translate(
                        "constitution_test.no_red_team_prompts", language
                    ),
                ).classes("principia-red-team-empty")
            else:
                ui.label(prompt.user).classes(
                    "principia-chat-bubble principia-chat-bubble-user",
                )
                ui.label(prompt.bot).classes(
                    "principia-chat-bubble principia-chat-bubble-bot",
                )

        ui.button(
            translator.translate("constitution_test.select_red_team_prompt", language),
            on_click=lambda: on_select_click(dialog),
        ).classes("principia-red-team-select").props(
            "flat no-caps" + (" disable" if prompt is None else ""),
        )


def _save_constitution(
    constitution: ConstitutionElement,
    example_hashes: list[str],
) -> None:
    updated_constitution = constitution.model_copy(
        update={"example_hashes": example_hashes},
    )
    payload = json.dumps(updated_constitution.model_dump())
    ui.run_javascript(
        f"""
        fetch('/api/supervised/constitution', {{
          method: 'PUT',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({payload}),
        }}).then((response) => {{
          if (!response.ok) throw new Error('Failed to save constitution test links');
          window.location.reload();
        }});
        """,
    )
