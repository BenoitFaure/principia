from principia.backend.chat import PromptTestChat, create_prompt_test_chat
from principia.backend.database import ConstitutionElement, DevElement, ExampleElement
from principia.services.openai_provider import ConversationInput, ConversationOutput


class FakeConversationProvider:
    def __init__(self, responses: list[str]) -> None:
        self._responses = responses
        self.calls: list[ConversationInput] = []

    def conversation(self, conversation_input: ConversationInput) -> ConversationOutput:
        self.calls.append(conversation_input)
        return ConversationOutput(message=self._responses.pop(0))


def test_generate_critique_sends_initial_prompt_with_examples() -> None:
    provider = FakeConversationProvider(["Critique output."])
    chat = create_prompt_test_chat(
        dev_element=_dev_element(),
        constitution_element=_constitution_element(),
        examples=[_example_element()],
        provider=provider,
        model="test-model",
    )

    response = chat.generate_critique()

    assert response == "Critique output."
    assert provider.calls[0].model == "test-model"
    assert provider.calls[0].messages[0].role == "user"
    assert provider.calls[0].messages[0].content == (
        "Extract from a conversation:\n"
        "USER: Red team user.\n"
        "ASSISTANT: Unsafe bot answer.\n\n"
        "A few examples of critique/response pairs:\n"
        "Example 1:\n"
        "USER: Example user.\n"
        "ASSISTANT: Example bot.\n"
        "CRITIQUE: Example critique.\n"
        "RESPONSE: Example response.\n\n"
        "Critique the assistant."
    )


def test_generate_critique_stores_user_prompt_and_assistant_reply() -> None:
    provider = FakeConversationProvider(["Critique output."])
    chat = create_prompt_test_chat(
        dev_element=_dev_element(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
    )

    chat.generate_critique()

    conversation = chat.conversation()
    assert [message.role for message in conversation] == ["user", "assistant"]
    assert conversation[1].content == "Critique output."


def test_generate_response_appends_response_prompt_and_assistant_reply() -> None:
    provider = FakeConversationProvider(["Critique output.", "Response output."])
    chat = create_prompt_test_chat(
        dev_element=_dev_element(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
    )

    chat.generate_critique()
    response = chat.generate_response()

    assert response == "Response output."
    conversation = chat.conversation()
    assert [message.role for message in conversation] == [
        "user",
        "assistant",
        "user",
        "assistant",
    ]
    assert conversation[2].content == "Improve the response."


def test_step_alternates_full_critique_response_and_short_critique() -> None:
    provider = FakeConversationProvider(
        ["Critique output.", "Response output.", "Second critique output."]
    )
    chat = create_prompt_test_chat(
        dev_element=_dev_element(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
    )

    first_step = chat.step()
    second_step = chat.step()
    third_step = chat.step()

    assert len(first_step) == 2
    assert first_step[0].content.startswith("Extract from a conversation:")
    assert len(second_step) == 4
    assert second_step[2].content == "Improve the response."
    assert len(third_step) == 6
    assert third_step[4].content == "Critique the assistant."


def test_step_keeps_alternating_after_third_call() -> None:
    provider = FakeConversationProvider(
        [
            "Critique output.",
            "Response output.",
            "Second critique output.",
            "Second response output.",
            "Third critique output.",
        ]
    )
    chat = create_prompt_test_chat(
        dev_element=_dev_element(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
    )

    for _ in range(5):
        conversation = chat.step()

    assert conversation[6].content == "Improve the response."
    assert conversation[8].content == "Critique the assistant."


def test_create_prompt_test_chat_returns_prompt_test_chat() -> None:
    chat = create_prompt_test_chat(
        dev_element=_dev_element(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=FakeConversationProvider([]),
    )

    assert isinstance(chat, PromptTestChat)


def _dev_element() -> DevElement:
    return DevElement(user="Red team user.", bot="Unsafe bot answer.")


def _constitution_element() -> ConstitutionElement:
    return ConstitutionElement(
        constitution_hash="constitution-1",
        critique_prompt="Critique the assistant.",
        response_prompt="Improve the response.",
        example_hashes=["example-1"],
    )


def _example_element() -> ExampleElement:
    return ExampleElement(
        example_hash="example-1",
        user="Example user.",
        bot="Example bot.",
        critique="Example critique.",
        response="Example response.",
    )
