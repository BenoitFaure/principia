"""Reusable edit dialog for supervised examples."""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any
from urllib.parse import quote

from nicegui import ui

from principia.backend.database import ExampleElement
from principia.services.translator import translator


def supervised_learning_example_edit(
    language: str,
    example: ExampleElement | None,
) -> Any:
    """Build an edit dialog for an existing or new example element."""
    element = example or _empty_example_element()

    with ui.dialog().classes("principia-example-edit-dialog") as dialog:
        with ui.card().classes("principia-example-edit-card"):
            ui.label(_dialog_title(language, example)).classes(
                "principia-example-edit-title",
            )
            user = ui.textarea(
                label=translator.translate("example_edit.user", language),
                value=element.user,
            ).classes("principia-example-edit-field")
            bot = ui.textarea(
                label=translator.translate("example_edit.bot", language),
                value=element.bot,
            ).classes("principia-example-edit-field")
            critique = ui.textarea(
                label=translator.translate("example_edit.critique", language),
                value=element.critique,
            ).classes("principia-example-edit-field")
            response = ui.textarea(
                label=translator.translate("example_edit.response", language),
                value=element.response,
            ).classes("principia-example-edit-field")

            with ui.row().classes("principia-example-edit-actions"):
                ui.button(
                    translator.translate("example_edit.delete", language),
                    on_click=lambda: _delete_example(dialog, element),
                ).classes(
                    "principia-example-edit-button principia-example-edit-delete",
                ).props("flat")
                ui.button(
                    translator.translate("example_edit.save", language),
                    on_click=lambda: _save_example(
                        dialog,
                        element,
                        str(user.value or ""),
                        str(bot.value or ""),
                        str(critique.value or ""),
                        str(response.value or ""),
                    ),
                ).classes(
                    "principia-example-edit-button principia-example-edit-save",
                ).props("flat")

    return dialog


def _save_example(
    dialog: Any,
    element: ExampleElement,
    user: str,
    bot: str,
    critique: str,
    response: str,
) -> None:
    updated_element = element.model_copy(
        update={
            "user": user,
            "bot": bot,
            "critique": critique,
            "response": response,
        },
    )
    payload = json.dumps(updated_element.model_dump())
    dialog.close()
    ui.run_javascript(
        f"""
        fetch('/api/supervised/examples', {{
          method: 'PUT',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({payload}),
        }}).then((response) => {{
          if (!response.ok) throw new Error('Failed to save example');
          window.location.reload();
        }});
        """,
    )


def _delete_example(dialog: Any, element: ExampleElement) -> None:
    example_hash = quote(element.example_hash, safe="")
    dialog.close()
    ui.run_javascript(
        f"""
        fetch('/api/supervised/examples/{example_hash}', {{
          method: 'DELETE',
        }}).then((response) => {{
          if (!response.ok) throw new Error('Failed to delete example');
          window.location.reload();
        }});
        """,
    )


def _empty_example_element() -> ExampleElement:
    seed = f"{datetime.now(UTC).isoformat()}:{random.randint(0, 1_000_000_000)}"
    return ExampleElement(
        example_hash=sha256(seed.encode("utf-8")).hexdigest(),
        user="",
        bot="",
        critique="",
        response="",
    )


def _dialog_title(language: str, example: ExampleElement | None) -> str:
    if example is None:
        return translator.translate("example_edit.create_title", language)
    return translator.translate("example_edit.edit_title", language)
