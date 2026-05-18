"""Supervised learning page for linking constitution critiques to examples."""

from __future__ import annotations

import json

from nicegui import ui

from principia.backend.database import (
    ConstitutionElement,
    ConstitutionFile,
    ExampleElement,
    ExamplesFile,
)
from principia.frontend.components.base_layout import base_two_pane_layout
from principia.frontend.components.supervised_learning_constitution_edit import (
    supervised_learning_constitution_edit as constitution_edit_dialog,
)
from principia.frontend.components.supervised_learning_example_edit import (
    supervised_learning_example_edit,
)
from principia.frontend.language import LearningStage, get_user_language
from principia.frontend.theme import apply_theme
from principia.services.translator import translator


def supervised_learning_constitution_edit_page() -> None:
    """Render the supervised learning constitution/example linking page."""
    language = get_user_language()
    apply_theme()

    constitutions = ConstitutionFile().read()
    examples = ExamplesFile().read()
    example_hashes = {example.example_hash for example in examples}
    selected_constitution_hash: str | None = None
    selected_example_hashes: set[str] = set()
    dirty = False

    def selected_constitution() -> ConstitutionElement | None:
        if selected_constitution_hash is None:
            return None
        return next(
            (
                constitution
                for constitution in constitutions
                if constitution.constitution_hash == selected_constitution_hash
            ),
            None,
        )

    def selected_context_examples(
        current_example: ExampleElement | None,
    ) -> list[ExampleElement]:
        constitution = selected_constitution()
        if constitution is None:
            return []

        current_hash = current_example.example_hash if current_example else None
        linked_hashes = set(constitution.example_hashes)
        return [
            example
            for example in examples
            if example.example_hash in linked_hashes
            and example.example_hash != current_hash
        ]

    def selected_hashes_in_example_order() -> list[str]:
        ordered_hashes = [
            example.example_hash
            for example in examples
            if example.example_hash in selected_example_hashes
        ]
        stale_hashes = sorted(selected_example_hashes - example_hashes)
        return ordered_hashes + stale_hashes

    def refresh_workspaces() -> None:
        constitution_workspace.refresh(language)
        examples_workspace.refresh(language)

    def select_constitution(constitution: ConstitutionElement) -> None:
        nonlocal dirty, selected_constitution_hash, selected_example_hashes

        if selected_constitution_hash != constitution.constitution_hash:
            selected_constitution_hash = constitution.constitution_hash
            selected_example_hashes = set(constitution.example_hashes)
            dirty = False
            refresh_workspaces()
            return

        if dirty:
            _save_selected_constitution(
                constitution,
                selected_hashes_in_example_order(),
            )
            return

        selected_constitution_hash = None
        selected_example_hashes = set()
        refresh_workspaces()

    def toggle_example(example: ExampleElement) -> None:
        nonlocal dirty
        constitution = selected_constitution()
        if constitution is None:
            ui.notify(
                translator.translate(
                    "constitution_link.select_critique_first",
                    language,
                ),
            )
            return

        if example.example_hash in selected_example_hashes:
            selected_example_hashes.remove(example.example_hash)
        else:
            selected_example_hashes.add(example.example_hash)

        dirty = selected_example_hashes != set(constitution.example_hashes)
        refresh_workspaces()

    @ui.refreshable
    def constitution_workspace(language: str) -> None:
        ui.label(
            translator.translate(
                "constitution_link.constitution_title",
                language,
            ),
        ).classes("principia-window-title")

        with ui.element("div").classes("principia-constitution-stack"):
            for constitution in constitutions:
                _constitution_link_widget(
                    language,
                    constitution,
                    selected_constitution_hash == constitution.constitution_hash,
                    dirty,
                    select_constitution,
                )

            create_dialog = constitution_edit_dialog(language, None)
            ui.button("+", on_click=create_dialog.open).classes(
                "principia-constitution-add",
            ).props("flat")

    @ui.refreshable
    def examples_workspace(language: str) -> None:
        selected = selected_constitution()
        _test_navigation(language, selected is not None)
        ui.label(
            translator.translate("constitution_link.examples_title", language),
        ).classes("principia-window-title")

        with ui.element("div").classes("principia-example-stack"):
            for example in examples:
                _example_link_widget(
                    language,
                    example,
                    selected,
                    selected_context_examples(example),
                    selected is not None,
                    example.example_hash in selected_example_hashes,
                    toggle_example,
                )

            create_dialog = supervised_learning_example_edit(
                language,
                None,
                selected,
                selected_context_examples(None),
            )
            ui.button("+", on_click=create_dialog.open).classes(
                "principia-example-add",
            ).props("flat")

    base_two_pane_layout(
        language,
        LearningStage.SUPERVISED,
        left_content=constitution_workspace,
        right_content=examples_workspace,
        stage_button_href="/",
    )


def _test_navigation(language: str, enabled: bool) -> None:
    button = ui.button(
        translator.translate("constitution_link.test_navigation", language),
    ).classes(
        "principia-edit-navigation-title"
        f" {'principia-edit-navigation-title-enabled' if enabled else ''}",
    )
    button.props("flat no-caps")
    if not enabled:
        button.props("disable")


def _constitution_link_widget(
    language: str,
    constitution: ConstitutionElement,
    selected: bool,
    dirty: bool,
    on_marker_click,
) -> None:
    edit_dialog = constitution_edit_dialog(language, constitution)
    preview = constitution.critique_prompt or translator.translate(
        "supervised_learning_main.empty_critique_prompt",
        language,
    )
    marker = "💾" if selected and dirty else "●" if selected else "○"
    marker_class = " principia-link-marker-dirty" if selected and dirty else ""
    widget_class = " principia-link-widget-selected" if selected else ""

    with ui.row().classes("principia-link-row"):
        ui.button(
            marker,
            on_click=lambda: on_marker_click(constitution),
        ).classes(f"principia-link-marker{marker_class}").props("flat")
        with (
            ui.button(on_click=edit_dialog.open)
            .classes(f"principia-constitution-widget{widget_class}")
            .props("flat no-caps")
        ):
            ui.label(preview).classes("principia-constitution-critique")


def _example_link_widget(
    language: str,
    example: ExampleElement,
    constitution: ConstitutionElement | None,
    examples: list[ExampleElement],
    critique_selected: bool,
    selected: bool,
    on_marker_click,
) -> None:
    edit_dialog = supervised_learning_example_edit(
        language,
        example,
        constitution,
        examples,
    )
    preview = example.user or translator.translate(
        "constitution_link.empty_user_prompt",
        language,
    )
    marker = "●" if selected else "○"
    marker_class = "" if critique_selected else " principia-link-marker-muted"
    widget_class = " principia-link-widget-selected" if selected else ""

    with ui.row().classes("principia-link-row"):
        ui.button(
            marker,
            on_click=lambda: on_marker_click(example),
        ).classes(f"principia-link-marker{marker_class}").props("flat")
        with (
            ui.button(on_click=edit_dialog.open)
            .classes(f"principia-example-widget{widget_class}")
            .props("flat no-caps")
        ):
            with ui.element("div").classes("principia-example-content"):
                ui.label(preview).classes("principia-example-user")
                ui.label(example.example_hash).classes("principia-example-hash")


def _save_selected_constitution(
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
          if (!response.ok) throw new Error('Failed to save constitution links');
          window.location.reload();
        }});
        """,
    )
