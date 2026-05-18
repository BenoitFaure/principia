"""Reusable edit dialog for supervised examples."""

from __future__ import annotations

import json
import random
from datetime import UTC, datetime
from hashlib import sha256
from typing import Any
from urllib.parse import quote

from nicegui import ui

from principia.backend.database import ConstitutionElement, ExampleElement
from principia.services.translator import translator


def supervised_learning_example_edit(
    language: str,
    example: ExampleElement | None,
    constitution: ConstitutionElement | None = None,
    examples: list[ExampleElement] | None = None,
) -> Any:
    """Build an edit dialog for an existing or new example element."""
    element = example or _empty_example_element()
    context_examples = examples or []
    chat_state = {
        "initialized": False,
        "critique_ready": False,
        "critique": "",
        "source_key": "",
    }

    with (
        ui.dialog()
        .classes("principia-example-edit-dialog")
        .props(
            "persistent",
        ) as dialog
    ):
        with ui.card().classes("principia-example-edit-card"):
            with ui.row().classes("principia-example-edit-header"):
                ui.label(_dialog_title(language, example)).classes(
                    "principia-example-edit-title",
                )
                ui.button(
                    "❌",
                    on_click=lambda: _close_dialog(dialog, chat_state),
                ).classes("principia-example-edit-close").props("flat")

            with ui.element("div").classes("principia-example-edit-body"):
                with ui.element("section").classes("principia-example-editor-pane"):
                    user = ui.textarea(
                        label=translator.translate("example_edit.user", language),
                        value=element.user,
                        on_change=lambda: _source_value_changed(
                            user,
                            bot,
                            critique,
                            create_critique_button,
                            create_response_button,
                            constitution,
                            chat_state,
                            chat_history,
                        ),
                    ).classes("principia-example-edit-field")
                    bot = ui.textarea(
                        label=translator.translate("example_edit.bot", language),
                        value=element.bot,
                        on_change=lambda: _source_value_changed(
                            user,
                            bot,
                            critique,
                            create_critique_button,
                            create_response_button,
                            constitution,
                            chat_state,
                            chat_history,
                        ),
                    ).classes("principia-example-edit-field")
                    critique = ui.textarea(
                        label=translator.translate("example_edit.critique", language),
                        value=element.critique,
                        on_change=lambda: _refresh_chat_actions(
                            user,
                            bot,
                            critique,
                            create_critique_button,
                            create_response_button,
                            constitution,
                        ),
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
                            "principia-example-edit-button "
                            "principia-example-edit-delete",
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

                with ui.element("section").classes("principia-example-chat-pane"):
                    ui.label(
                        translator.translate("example_edit.refinement_title", language),
                    ).classes("principia-example-chat-title")
                    if constitution is None:
                        ui.label(
                            translator.translate(
                                "example_edit.select_constitution_hint",
                                language,
                            ),
                        ).classes("principia-example-chat-hint")

                    chat_history = ui.column().classes("principia-example-chat-history")

                    with ui.row().classes("principia-example-chat-send-row"):
                        message_input = ui.input(
                            placeholder=translator.translate(
                                "example_edit.chat_placeholder",
                                language,
                            ),
                        ).classes("principia-example-chat-input")
                        ui.button(
                            "➤",
                            on_click=lambda: _send_chat_message(
                                element,
                                user,
                                bot,
                                critique,
                                response,
                                constitution,
                                context_examples,
                                message_input,
                                chat_history,
                                chat_state,
                                language,
                            ),
                        ).classes("principia-example-chat-send").props("flat")

                    with ui.row().classes("principia-example-chat-actions"):
                        create_critique_button = (
                            ui.button(
                                translator.translate(
                                    "example_edit.create_critique",
                                    language,
                                ),
                                on_click=lambda: _create_critique(
                                    element,
                                    user,
                                    bot,
                                    critique,
                                    response,
                                    constitution,
                                    context_examples,
                                    chat_history,
                                    chat_state,
                                    create_response_button,
                                    language,
                                ),
                            )
                            .classes("principia-example-chat-action")
                            .props("flat")
                        )
                        create_response_button = (
                            ui.button(
                                translator.translate(
                                    "example_edit.create_response",
                                    language,
                                ),
                                on_click=lambda: _create_response(
                                    element,
                                    user,
                                    bot,
                                    critique,
                                    response,
                                    constitution,
                                    context_examples,
                                    chat_history,
                                    chat_state,
                                    language,
                                ),
                            )
                            .classes("principia-example-chat-action")
                            .props("flat")
                        )

            _refresh_chat_actions(
                user,
                bot,
                critique,
                create_critique_button,
                create_response_button,
                constitution,
            )

    return dialog


async def _close_dialog(dialog: Any, chat_state: dict[str, object]) -> None:
    await _reset_refinement_chat(chat_state)
    dialog.close()


def _refresh_chat_actions(
    user: Any,
    bot: Any,
    critique: Any,
    create_critique_button: Any,
    create_response_button: Any,
    constitution: ConstitutionElement | None,
) -> None:
    has_constitution = constitution is not None
    has_conversation = bool(str(user.value or "").strip()) and bool(
        str(bot.value or "").strip()
    )
    has_critique = bool(str(critique.value or "").strip())

    _set_enabled(create_critique_button, has_constitution and has_conversation)
    _set_enabled(
        create_response_button,
        has_constitution and has_conversation and has_critique,
    )


def _set_enabled(element: Any, enabled: bool) -> None:
    if enabled:
        element.enable()
        return
    element.disable()


async def _source_value_changed(
    user: Any,
    bot: Any,
    critique: Any,
    create_critique_button: Any,
    create_response_button: Any,
    constitution: ConstitutionElement | None,
    chat_state: dict[str, object],
    chat_history: Any,
) -> None:
    _refresh_chat_actions(
        user,
        bot,
        critique,
        create_critique_button,
        create_response_button,
        constitution,
    )
    await _reset_refinement_chat(chat_state)
    chat_history.clear()


async def _create_critique(
    element: ExampleElement,
    user: Any,
    bot: Any,
    critique: Any,
    response: Any,
    constitution: ConstitutionElement | None,
    examples: list[ExampleElement],
    chat_history: Any,
    chat_state: dict[str, object],
    create_response_button: Any,
    language: str,
) -> None:
    if constitution is None:
        ui.notify(
            translator.translate("example_edit.select_constitution_hint", language),
        )
        return
    if not _has_user_and_bot(user, bot):
        return

    await _reset_refinement_chat(chat_state)
    chat_history.clear()
    await _ensure_refinement_chat(
        element,
        user,
        bot,
        critique,
        response,
        constitution,
        examples,
        chat_state,
    )
    message = await _api_json("POST", "/api/chat/example-refinement/critique")
    content = str(message["content"])
    critique.value = content
    critique.update()
    chat_state["critique_ready"] = True
    chat_state["critique"] = content
    _set_enabled(create_response_button, True)
    _append_chat_bubble(chat_history, str(message["role"]), content)


async def _create_response(
    element: ExampleElement,
    user: Any,
    bot: Any,
    critique: Any,
    response: Any,
    constitution: ConstitutionElement | None,
    examples: list[ExampleElement],
    chat_history: Any,
    chat_state: dict[str, object],
    language: str,
) -> None:
    if constitution is None:
        ui.notify(
            translator.translate("example_edit.select_constitution_hint", language),
        )
        return
    if not _has_user_and_bot(user, bot):
        return

    await _ensure_refinement_chat(
        element,
        user,
        bot,
        critique,
        response,
        constitution,
        examples,
        chat_state,
    )
    current_critique = str(critique.value or "").strip()
    if not current_critique:
        return

    if not chat_state["critique_ready"]:
        await _api_json("POST", "/api/chat/example-refinement/critique")
        chat_state["critique_ready"] = True

    if current_critique and current_critique != chat_state["critique"]:
        message = await _api_json(
            "PUT",
            "/api/chat/example-refinement/critique",
            {"critique": current_critique},
        )
        chat_state["critique"] = current_critique
        _append_chat_bubble(chat_history, str(message["role"]), str(message["content"]))

    message = await _api_json("POST", "/api/chat/example-refinement/response")
    content = str(message["content"])
    response.value = _extract_obtained_response(content)
    response.update()
    _append_chat_bubble(chat_history, str(message["role"]), content)


async def _send_chat_message(
    element: ExampleElement,
    user: Any,
    bot: Any,
    critique: Any,
    response: Any,
    constitution: ConstitutionElement | None,
    examples: list[ExampleElement],
    message_input: Any,
    chat_history: Any,
    chat_state: dict[str, object],
    language: str,
) -> None:
    message = str(message_input.value or "").strip()
    if not message:
        return
    if constitution is None:
        ui.notify(
            translator.translate("example_edit.select_constitution_hint", language),
        )
        return

    await _ensure_refinement_chat(
        element,
        user,
        bot,
        critique,
        response,
        constitution,
        examples,
        chat_state,
    )

    message_input.value = ""
    message_input.update()
    _append_chat_bubble(chat_history, "user", message)
    response = await _api_json(
        "POST",
        "/api/chat/example-refinement/message",
        {"content": message},
    )
    _append_chat_bubble(chat_history, str(response["role"]), str(response["content"]))


def _has_user_and_bot(user: Any, bot: Any) -> bool:
    return bool(str(user.value or "").strip()) and bool(str(bot.value or "").strip())


async def _ensure_refinement_chat(
    element: ExampleElement,
    user: Any,
    bot: Any,
    critique: Any,
    response: Any,
    constitution: ConstitutionElement,
    examples: list[ExampleElement],
    chat_state: dict[str, object],
) -> None:
    source_key = _chat_source_key(element, user, bot, constitution, examples)
    if chat_state["initialized"] and chat_state["source_key"] == source_key:
        return

    if chat_state["initialized"]:
        await _reset_refinement_chat(chat_state)

    payload = {
        "example": _example_payload(element, user, bot, critique, response),
        "constitution_element": constitution.model_dump(),
        "examples": [
            example.model_dump()
            for example in examples
            if example.example_hash != element.example_hash
        ],
    }
    await _api_json("POST", "/api/chat/example-refinement/init", payload)
    chat_state["initialized"] = True
    chat_state["critique_ready"] = False
    chat_state["critique"] = ""
    chat_state["source_key"] = source_key


async def _reset_refinement_chat(chat_state: dict[str, object]) -> None:
    if chat_state["initialized"]:
        await _delete_refinement_chat()
    chat_state["initialized"] = False
    chat_state["critique_ready"] = False
    chat_state["critique"] = ""
    chat_state["source_key"] = ""


def _chat_source_key(
    element: ExampleElement,
    user: Any,
    bot: Any,
    constitution: ConstitutionElement,
    examples: list[ExampleElement],
) -> str:
    return json.dumps(
        {
            "example_hash": element.example_hash,
            "user": str(user.value or ""),
            "bot": str(bot.value or ""),
            "constitution": constitution.model_dump(),
            "examples": [example.model_dump() for example in examples],
        },
        sort_keys=True,
    )


def _example_payload(
    element: ExampleElement,
    user: Any,
    bot: Any,
    critique: Any,
    response: Any,
) -> dict[str, str]:
    return {
        "example_hash": element.example_hash,
        "user": str(user.value or ""),
        "bot": str(bot.value or ""),
        "critique": str(critique.value or ""),
        "response": str(response.value or ""),
    }


async def _api_json(
    method: str,
    path: str,
    payload: dict[str, object] | None = None,
) -> Any:
    body = ""
    headers = ""
    if payload is not None:
        headers = "headers: {'Content-Type': 'application/json'},"
        body = f"body: JSON.stringify({json.dumps(payload)}),"

    return await ui.run_javascript(
        f"""
        return await (async () => {{
          const response = await fetch({json.dumps(path)}, {{
            method: {json.dumps(method)},
            {headers}
            {body}
          }});
          if (!response.ok) {{
            throw new Error(await response.text());
          }}
          return await response.json();
        }})();
        """,
        timeout=30,
    )


async def _delete_refinement_chat() -> None:
    try:
        await _api_json("DELETE", "/api/chat/example-refinement")
    except Exception:
        pass


def _append_chat_bubble(chat_history: Any, role: str, content: str) -> None:
    bubble_class = "principia-example-chat-bubble-assistant"
    if role == "user":
        bubble_class = "principia-example-chat-bubble-user"

    with chat_history:
        ui.label(content).classes(f"principia-example-chat-bubble {bubble_class}")


def _extract_obtained_response(content: str) -> str:
    marker = "Obtained response:\n"
    if marker not in content:
        return content
    return content.split(marker, maxsplit=1)[1]


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
        fetch('/api/chat/example-refinement', {{method: 'DELETE'}})
          .catch(() => undefined);
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
        fetch('/api/chat/example-refinement', {{method: 'DELETE'}})
          .catch(() => undefined);
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
