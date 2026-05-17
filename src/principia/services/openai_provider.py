"""OpenAI SDK provider for conversation requests."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Literal, cast

from openai import OpenAI
from pydantic import BaseModel

OPENAI_KEY_NOT_SET = "OpenAI key not set"


class ConversationMessage(BaseModel):
    """A single message in an OpenAI chat conversation."""

    role: Literal["system", "user", "assistant"]
    content: str


class ConversationInput(BaseModel):
    """Input for an OpenAI chat conversation."""

    messages: list[ConversationMessage]
    model: str = "gpt-4o-mini"


class ConversationOutput(BaseModel):
    """Output containing the assistant response text."""

    message: str


class OpenAIProvider:
    """Manage an OpenAI client and send conversation requests."""

    def __init__(
        self,
        client_factory: Callable[[str], OpenAI] | None = None,
    ) -> None:
        if client_factory is None:
            client_factory = _create_openai_client
        self._client_factory = client_factory
        self._client: OpenAI | None = None

    def update_api_key(self, api_key: str) -> None:
        """Create or clear the OpenAI client for an API key."""
        stripped_api_key = api_key.strip()
        if not stripped_api_key:
            self._client = None
            return

        self._client = self._client_factory(stripped_api_key)

    def is_set(self) -> bool:
        """Return whether an OpenAI client has been configured."""
        return self._client is not None

    def conversation(self, conversation_input: ConversationInput) -> ConversationOutput:
        """Send a conversation to OpenAI and return the assistant message."""
        client = self._client
        if client is None:
            return ConversationOutput(message=OPENAI_KEY_NOT_SET)

        response = client.chat.completions.create(
            model=conversation_input.model,
            messages=cast(
                Any,
                [message.model_dump() for message in conversation_input.messages],
            ),
        )
        return ConversationOutput(message=response.choices[0].message.content or "")


def _create_openai_client(api_key: str) -> OpenAI:
    return OpenAI(api_key=api_key)


openai_provider = OpenAIProvider()
