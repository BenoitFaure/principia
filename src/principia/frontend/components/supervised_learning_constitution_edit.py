"""Reusable edit dialog for supervised constitution elements."""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any
from urllib.parse import quote

from nicegui import ui

from principia.backend.database import ConstitutionElement
from principia.services.translator import translator


def supervised_learning_constitution_edit(
    language: str,
    constitution: ConstitutionElement | None,
) -> Any:
    """Build an edit dialog for an existing or new constitution element."""
    element = constitution or _empty_constitution_element()

    with ui.dialog().classes("principia-constitution-edit-dialog") as dialog:
        with ui.card().classes("principia-constitution-edit-card"):
            ui.label(_dialog_title(language, constitution)).classes(
                "principia-constitution-edit-title",
            )
            critique_prompt = ui.textarea(
                label=translator.translate(
                    "constitution_edit.critique_prompt",
                    language,
                ),
                value=element.critique_prompt,
            ).classes("principia-constitution-edit-field")
            response_prompt = ui.textarea(
                label=translator.translate(
                    "constitution_edit.response_prompt",
                    language,
                ),
                value=element.response_prompt,
            ).classes("principia-constitution-edit-field")

            with ui.row().classes("principia-constitution-edit-actions"):
                ui.button(
                    translator.translate("constitution_edit.delete", language),
                    on_click=lambda: _delete_constitution(dialog, element),
                ).classes(
                    "principia-constitution-edit-button "
                    "principia-constitution-edit-delete",
                ).props("flat")
                ui.button(
                    translator.translate("constitution_edit.save", language),
                    on_click=lambda: _save_constitution(
                        dialog,
                        element,
                        str(critique_prompt.value or ""),
                        str(response_prompt.value or ""),
                    ),
                ).classes(
                    "principia-constitution-edit-button "
                    "principia-constitution-edit-save",
                ).props("flat")

    return dialog


def _save_constitution(
    dialog: Any,
    element: ConstitutionElement,
    critique_prompt: str,
    response_prompt: str,
) -> None:
    updated_element = element.model_copy(
        update={
            "critique_prompt": critique_prompt,
            "response_prompt": response_prompt,
        },
    )
    payload = json.dumps(updated_element.model_dump())
    hash_value = json.dumps(updated_element.constitution_hash)
    dialog.close()
    ui.run_javascript(
        f"""
        fetch('/api/supervised/constitution', {{
          method: 'PUT',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({payload}),
        }}).then((response) => {{
          if (!response.ok) throw new Error('Failed to save constitution');
          localStorage.setItem('principia_selected_constitution', {hash_value});
          window.location.reload();
        }});
        """,
    )


def _delete_constitution(dialog: Any, element: ConstitutionElement) -> None:
    constitution_hash = quote(element.constitution_hash, safe="")
    dialog.close()
    ui.run_javascript(
        f"""
        fetch('/api/supervised/constitution/{constitution_hash}', {{
          method: 'DELETE',
        }}).then((response) => {{
          if (!response.ok) throw new Error('Failed to delete constitution');
          window.location.reload();
        }});
        """,
    )


def _empty_constitution_element() -> ConstitutionElement:
    seed = f"{datetime.now(UTC).isoformat()}:{random.randint(0, 1_000_000_000)}"
    return ConstitutionElement(
        constitution_hash=sha256(seed.encode("utf-8")).hexdigest(),
        critique_prompt="",
        response_prompt="",
        example_hashes=[],
    )


def _dialog_title(language: str, constitution: ConstitutionElement | None) -> str:
    if constitution is None:
        return translator.translate("constitution_edit.create_title", language)
    return translator.translate("constitution_edit.edit_title", language)
