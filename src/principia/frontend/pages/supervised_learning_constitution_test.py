"""Supervised learning page for testing one constitution critique."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

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
from principia.frontend.components.supervised_learning_constitution_edit import (
    supervised_learning_constitution_edit as constitution_edit_dialog,
)
from principia.frontend.language import LearningStage, get_user_language
from principia.frontend.theme import apply_theme
from principia.services.open_ai.models import AVAILABLE_MODELS, DEFAULT_MODEL
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
    extra_example_hashes: set[str] = set()
    red_team_element: DevElement | None = None
    conversation_messages: list[dict] = []
    loading: bool = False
    model_state = {"value": DEFAULT_MODEL}

    ui.run_javascript("""
      document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'hidden') {
          fetch('/api/chat/prompt-test', {method: 'DELETE'}).catch(() => {});
        }
      });
    """)

    def selected_hashes_in_example_order() -> list[str]:
        ordered_hashes = [
            example.example_hash
            for example in examples
            if example.example_hash in selected_example_hashes
        ]
        stale_hashes = sorted(selected_example_hashes - example_hashes)
        return ordered_hashes + stale_hashes

    def displayed_examples() -> list[ExampleElement]:
        displayed_hashes = (
            set(constitution.example_hashes) if constitution is not None else set()
        ) | extra_example_hashes
        return [e for e in examples if e.example_hash in displayed_hashes]

    def toggle_example(example: ExampleElement) -> None:
        if example.example_hash in selected_example_hashes:
            selected_example_hashes.remove(example.example_hash)
        else:
            selected_example_hashes.add(example.example_hash)

        critique_workspace.refresh(language)

    def add_example(example: ExampleElement) -> None:
        extra_example_hashes.add(example.example_hash)
        selected_example_hashes.add(example.example_hash)
        critique_workspace.refresh(language)

    def select_red_team_prompt(prompt: DevElement, dialog) -> None:
        nonlocal red_team_element, conversation_messages, loading
        red_team_element = prompt
        conversation_messages = []
        loading = False
        dialog.close()
        red_team_workspace.refresh(language)

    def _scroll_chat_to_bottom() -> None:
        ui.run_javascript("""
          setTimeout(() => {
            const el = document.querySelector('.principia-prompt-test-chat');
            if (el) el.scrollTop = el.scrollHeight;
          }, 50);
        """)

    def do_reset() -> None:
        nonlocal conversation_messages, loading
        conversation_messages = []
        loading = False
        ui.run_javascript(
            "fetch('/api/chat/prompt-test', {method: 'DELETE'}).catch(() => {});"
        )
        red_team_workspace.refresh(language)

    async def do_critique() -> None:
        nonlocal conversation_messages, loading
        if constitution is None or red_team_element is None:
            return
        loading = True
        red_team_workspace.refresh(language)
        examples_for_init = [
            e for e in examples if e.example_hash in selected_example_hashes
        ]
        init_payload = {
            "dev_element": red_team_element.model_dump(),
            "constitution_element": constitution.model_dump(),
            "examples": [e.model_dump() for e in examples_for_init],
            "model": model_state["value"],
        }
        try:
            await ui.run_javascript(
                f"""
                return await (async () => {{
                  const r = await fetch('/api/chat/prompt-test/init', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({json.dumps(init_payload)}),
                  }});
                  if (!r.ok) throw new Error(await r.text());
                  return await r.json();
                }})();
                """,
                timeout=30,
            )
            await ui.run_javascript(
                """
                return await (async () => {
                  const r = await fetch('/api/chat/prompt-test/critique', {method: 'POST'});
                  if (!r.ok) throw new Error(await r.text());
                  return await r.json();
                })();
                """,
                timeout=60,
            )
            result = await ui.run_javascript(
                """
                return await (async () => {
                  const r = await fetch('/api/chat/prompt-test');
                  if (!r.ok) throw new Error(await r.text());
                  return await r.json();
                })();
                """,
                timeout=10,
            )
            conversation_messages = result
        except Exception as e:
            ui.notify(str(e))
        finally:
            loading = False
        red_team_workspace.refresh(language)
        _scroll_chat_to_bottom()

    async def do_response() -> None:
        nonlocal conversation_messages, loading
        loading = True
        red_team_workspace.refresh(language)
        try:
            await ui.run_javascript(
                """
                return await (async () => {
                  const r = await fetch('/api/chat/prompt-test/response', {method: 'POST'});
                  if (!r.ok) throw new Error(await r.text());
                  return await r.json();
                })();
                """,
                timeout=60,
            )
            result = await ui.run_javascript(
                """
                return await (async () => {
                  const r = await fetch('/api/chat/prompt-test');
                  if (!r.ok) throw new Error(await r.text());
                  return await r.json();
                })();
                """,
                timeout=10,
            )
            conversation_messages = result
        except Exception as e:
            ui.notify(str(e))
        finally:
            loading = False
        red_team_workspace.refresh(language)
        _scroll_chat_to_bottom()

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
            for example in displayed_examples():
                _example_test_widget(
                    language,
                    example,
                    example.example_hash in selected_example_hashes,
                    toggle_example,
                )

            select_dialog = _example_select_dialog(
                language,
                examples,
                selected_example_hashes,
                extra_example_hashes,
                add_example,
            )
            ui.button("+", on_click=select_dialog.open).classes(
                "principia-example-add",
            ).props("flat")

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

        ui.select(
            AVAILABLE_MODELS,
            value=model_state["value"],
            label=translator.translate("constitution_test.teacher_model", language),
            on_change=lambda e: model_state.update({"value": e.value}),
        ).classes("principia-model-selector")

        _red_team_selector_widget(language, dev_prompts, select_red_team_prompt)

        if red_team_element is not None:
            disable_prop = " disable" if loading else ""
            ui.button(
                translator.translate("constitution_test.reset_button", language),
                on_click=do_reset,
            ).classes("principia-prompt-test-reset").props(
                f"flat no-caps{disable_prop}"
            )

            with ui.element("div").classes("principia-prompt-test-chat"):
                ui.label(red_team_element.user).classes(
                    "principia-chat-bubble principia-chat-bubble-user"
                )
                ui.label(red_team_element.bot).classes(
                    "principia-chat-bubble principia-chat-bubble-bot"
                )
                for i, msg in enumerate(conversation_messages):
                    if i == 1:
                        ui.label(
                            translator.translate(
                                "constitution_test.critique_button", language
                            )
                        ).classes(
                            "principia-chat-section-label"
                            " principia-chat-section-label-critique"
                        )
                    elif i == 3:
                        ui.label(
                            translator.translate(
                                "constitution_test.response_button", language
                            )
                        ).classes("principia-chat-section-label")
                    bubble_class = (
                        "principia-chat-bubble-user"
                        if msg["role"] == "user"
                        else "principia-chat-bubble-bot"
                    )
                    ui.label(msg["content"]).classes(
                        f"principia-chat-bubble {bubble_class}"
                    )
                if loading:
                    ui.label(
                        translator.translate(
                            "constitution_test.loading_message", language
                        )
                    ).classes("principia-prompt-test-loading")

            if len(conversation_messages) == 0:
                ui.button(
                    translator.translate("constitution_test.critique_button", language),
                    on_click=do_critique,
                ).classes("principia-prompt-test-action").props(
                    f"flat no-caps{disable_prop}"
                )
            elif len(conversation_messages) == 2:
                ui.button(
                    translator.translate("constitution_test.response_button", language),
                    on_click=do_response,
                ).classes("principia-prompt-test-action").props(
                    f"flat no-caps{disable_prop}"
                )

    base_two_pane_layout(
        language,
        LearningStage.SUPERVISED,
        left_content=critique_workspace,
        right_content=red_team_workspace,
        stage_button_href="/",
    )


def _red_team_selector_widget(
    language: str,
    dev_prompts: list[DevElement],
    on_prompt_click,
) -> None:
    dialog = _red_team_prompt_dialog(language, dev_prompts, on_prompt_click)
    ui.button(
        translator.translate("constitution_test.select_prompt_button", language),
        on_click=dialog.open,
    ).classes("principia-red-team-selector-button").props("flat no-caps")


def _constitution_test_widget(
    language: str,
    constitution: ConstitutionElement,
    selected_hashes: Callable[[], list[str]],
) -> None:
    edit_dialog = constitution_edit_dialog(language, constitution)
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
        with (
            ui.button(on_click=edit_dialog.open)
            .classes("principia-constitution-widget")
            .props("flat no-caps")
        ):
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


def _example_select_dialog(
    language: str,
    all_examples: list[ExampleElement],
    selected_hashes: set[str],
    extra_hashes: set[str],
    on_add: Callable[[ExampleElement], None],
) -> Any:
    previewed_example: ExampleElement | None = all_examples[0] if all_examples else None

    def preview_or_add(example: ExampleElement, dialog) -> None:
        nonlocal previewed_example
        if example == previewed_example:
            on_add(example)
            dialog.close()
            return
        previewed_example = example
        select_dialog_content.refresh(language, dialog)

    def add_previewed(dialog) -> None:
        if previewed_example is not None:
            on_add(previewed_example)
            dialog.close()

    @ui.refreshable
    def select_dialog_content(language: str, dialog) -> None:
        ui.label(
            translator.translate("constitution_test.example_select_title", language),
        ).classes("principia-red-team-title")
        with ui.element("div").classes("principia-red-team-selector"):
            with ui.element("div").classes("principia-red-team-list"):
                for ex in all_examples:
                    already = ex.example_hash in selected_hashes
                    _example_list_widget(
                        language,
                        ex,
                        ex == previewed_example,
                        already,
                        dialog,
                        preview_or_add,
                    )
            _example_detail_pane(language, previewed_example, dialog, add_previewed)

    with ui.dialog().classes("principia-red-team-dialog") as dialog:
        with ui.card().classes("principia-example-select-card"):
            select_dialog_content(language, dialog)

    return dialog


def _example_list_widget(
    language: str,
    example: ExampleElement,
    previewed: bool,
    already_selected: bool,
    dialog,
    on_click,
) -> None:
    preview = example.user or translator.translate(
        "constitution_link.empty_user_prompt",
        language,
    )
    widget_class = "principia-dev-prompt-widget"
    if previewed:
        widget_class += " principia-dev-prompt-widget-selected"
    if already_selected:
        widget_class += " principia-link-marker-selected"

    with (
        ui.button(on_click=lambda: on_click(example, dialog))
        .classes(widget_class)
        .props("flat no-caps")
    ):
        ui.label(preview).classes("principia-dev-prompt-user")
        ui.label(example.example_hash).classes("principia-example-hash")


def _example_detail_pane(
    language: str,
    example: ExampleElement | None,
    dialog,
    on_add_click,
) -> None:
    with ui.element("div").classes("principia-red-team-chat"):
        with ui.element("div").classes("principia-red-team-chat-messages"):
            if example is None:
                ui.label(
                    translator.translate(
                        "constitution_test.no_red_team_prompts", language
                    ),
                ).classes("principia-red-team-empty")
            else:
                for field_key, value in [
                    ("example_edit.user", example.user),
                    ("example_edit.bot", example.bot),
                    ("example_edit.critique", example.critique),
                    ("example_edit.response", example.response),
                ]:
                    ui.label(translator.translate(field_key, language)).classes(
                        "principia-example-detail-label"
                    )
                    ui.label(value or "—").classes("principia-example-detail-value")

        ui.button(
            translator.translate("constitution_test.example_select_action", language),
            on_click=lambda: on_add_click(dialog),
        ).classes("principia-red-team-select").props(
            "flat no-caps" + (" disable" if example is None else ""),
        )


def _red_team_prompt_dialog(
    language: str,
    dev_prompts: list[DevElement],
    on_prompt_click,
) -> Any:
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
