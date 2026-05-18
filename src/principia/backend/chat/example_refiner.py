from principia.backend.database import ConstitutionElement, DevElement, ExampleElement
from principia.services.openai_provider import (
    ConversationInput,
    ConversationMessage,
    openai_provider,
)

from .prompt_tester import ConversationProvider, PromptTestChat


class ExampleRefinementChat:
    def __init__(
        self,
        *,
        example: ExampleElement,
        constitution_element: ConstitutionElement,
        examples: list[ExampleElement],
        provider: ConversationProvider = openai_provider,
        model: str = "gpt-4o-mini",
    ) -> None:
        self._provider = provider
        self._model = model
        self._prompt_test_chat = PromptTestChat(
            dev_element=DevElement(user=example.user, bot=example.bot),
            constitution_element=constitution_element,
            examples=examples,
            provider=provider,
            model=model,
        )
        self._conversation: list[ConversationMessage] = []
        self._critique_message_index: int | None = None
        self._response_message_index: int | None = None

    def conversation(self) -> list[ConversationMessage]:
        return list(self._conversation)

    def get_critique(self) -> ConversationMessage:
        critique = self._prompt_test_chat.generate_critique()
        message = ConversationMessage(role="assistant", content=critique)
        self._conversation.append(message)
        self._critique_message_index = len(self._conversation) - 1
        self._response_message_index = None
        return message

    def update_critique(self, critique: str) -> ConversationMessage:
        self._prompt_test_chat.update_critique(critique)
        message = ConversationMessage(role="assistant", content=critique)

        if self._critique_message_index is None:
            self._conversation.append(message)
            self._critique_message_index = len(self._conversation) - 1
            return message

        self._conversation[self._critique_message_index] = message
        self._clear_stale_response()
        return message

    def get_response(self) -> ConversationMessage:
        critique = self._prompt_test_chat.critique()
        if critique is None:
            critique = self.get_critique().content

        response = self._prompt_test_chat.generate_response()
        message = ConversationMessage(
            role="assistant",
            content=f"Using Critique:\n{critique}\n\nObtained response:\n{response}",
        )
        self._conversation.append(message)
        self._response_message_index = len(self._conversation) - 1
        return message

    def message(self, content: str) -> ConversationMessage:
        self._conversation.append(ConversationMessage(role="user", content=content))
        output = self._provider.conversation(
            ConversationInput(messages=self.conversation(), model=self._model)
        )
        message = ConversationMessage(role="assistant", content=output.message)
        self._conversation.append(message)
        return message

    def _clear_stale_response(self) -> None:
        if (
            self._response_message_index is None
            or self._critique_message_index is None
            or self._response_message_index < self._critique_message_index
        ):
            return

        del self._conversation[self._response_message_index :]
        self._response_message_index = None


def create_example_refinement_chat(
    example: ExampleElement,
    constitution_element: ConstitutionElement,
    examples: list[ExampleElement],
    *,
    provider: ConversationProvider = openai_provider,
    model: str = "gpt-4o-mini",
) -> ExampleRefinementChat:
    return ExampleRefinementChat(
        example=example,
        constitution_element=constitution_element,
        examples=examples,
        provider=provider,
        model=model,
    )
