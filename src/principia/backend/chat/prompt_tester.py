from typing import Protocol

from principia.backend.database import ConstitutionElement, DevElement, ExampleElement
from principia.services.openai_provider import (
    ConversationInput,
    ConversationMessage,
    ConversationOutput,
    openai_provider,
)


class ConversationProvider(Protocol):
    def conversation(
        self, conversation_input: ConversationInput
    ) -> ConversationOutput: ...


class PromptTestChat:
    def __init__(
        self,
        *,
        dev_element: DevElement,
        constitution_element: ConstitutionElement,
        examples: list[ExampleElement],
        provider: ConversationProvider = openai_provider,
        model: str = "gpt-4o-mini",
    ) -> None:
        self._dev_element = dev_element
        self._constitution_element = constitution_element
        self._examples = examples
        self._provider = provider
        self._model = model
        self._conversation: list[ConversationMessage] = []
        self._step_count = 0
        self._critique_message_index: int | None = None
        self._response_prompt_index: int | None = None
        self._response_message_index: int | None = None

    def conversation(self) -> list[ConversationMessage]:
        return list(self._conversation)

    def critique(self) -> str | None:
        if self._critique_message_index is None:
            return None
        return self._conversation[self._critique_message_index].content

    def update_critique(self, critique: str) -> None:
        if self._critique_message_index is None:
            msg = "Cannot update critique before generating one."
            raise RuntimeError(msg)

        self._conversation[self._critique_message_index] = ConversationMessage(
            role="assistant",
            content=critique,
        )
        self._clear_response_after_updated_critique()

    def generate_critique(self) -> str:
        critique = self._send_user_message(self._initial_critique_prompt())
        self._critique_message_index = len(self._conversation) - 1
        self._response_prompt_index = None
        self._response_message_index = None
        return critique

    def generate_response(self) -> str:
        self._response_prompt_index = len(self._conversation)
        response = self._send_user_message(self._constitution_element.response_prompt)
        self._response_message_index = len(self._conversation) - 1
        return response

    def step(self) -> list[ConversationMessage]:
        if self._step_count == 0:
            self.generate_critique()
        elif self._step_count % 2 == 1:
            self.generate_response()
        else:
            self._send_user_message(self._constitution_element.critique_prompt)
            self._critique_message_index = len(self._conversation) - 1
            self._response_prompt_index = None
            self._response_message_index = None

        self._step_count += 1
        return self.conversation()

    def _clear_response_after_updated_critique(self) -> None:
        if (
            self._critique_message_index is None
            or self._response_prompt_index is None
            or self._response_message_index is None
            or self._response_prompt_index < self._critique_message_index
        ):
            return

        del self._conversation[self._response_prompt_index :]
        self._response_prompt_index = None
        self._response_message_index = None
        self._step_count = len(self._conversation) // 2

    def _send_user_message(self, prompt: str) -> str:
        self._conversation.append(ConversationMessage(role="user", content=prompt))
        output = self._provider.conversation(
            ConversationInput(messages=self.conversation(), model=self._model)
        )
        self._conversation.append(
            ConversationMessage(role="assistant", content=output.message)
        )
        return output.message

    def _initial_critique_prompt(self) -> str:
        return (
            "Extract from a conversation:\n"
            f"USER: {self._dev_element.user}\n"
            f"ASSISTANT: {self._dev_element.bot}\n\n"
            "A few examples of critique/response pairs:\n"
            f"{self._format_examples()}\n\n"
            f"{self._constitution_element.critique_prompt}"
        )

    def _format_examples(self) -> str:
        return "\n\n".join(
            _format_example(index=index, example=example)
            for index, example in enumerate(self._examples, start=1)
        )


def create_prompt_test_chat(
    dev_element: DevElement,
    constitution_element: ConstitutionElement,
    examples: list[ExampleElement],
    *,
    provider: ConversationProvider = openai_provider,
    model: str = "gpt-4o-mini",
) -> PromptTestChat:
    return PromptTestChat(
        dev_element=dev_element,
        constitution_element=constitution_element,
        examples=examples,
        provider=provider,
        model=model,
    )


def _format_example(*, index: int, example: ExampleElement) -> str:
    return (
        f"Example {index}:\n"
        f"USER: {example.user}\n"
        f"ASSISTANT: {example.bot}\n"
        f"CRITIQUE: {example.critique}\n"
        f"RESPONSE: {example.response}"
    )
