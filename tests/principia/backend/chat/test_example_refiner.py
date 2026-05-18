import pytest

from principia.backend.chat import ExampleRefinementChat, create_example_refinement_chat
from principia.backend.database import ConstitutionElement, ExampleElement
from principia.services.openai_provider import ConversationInput, ConversationOutput


class FakeConversationProvider:
    def __init__(self, responses: list[str]) -> None:
        self._responses = responses
        self.calls: list[ConversationInput] = []

    def conversation(self, conversation_input: ConversationInput) -> ConversationOutput:
        self.calls.append(conversation_input)
        return ConversationOutput(message=self._responses.pop(0))


def test_get_critique_returns_assistant_message_and_stores_it() -> None:
    provider = FakeConversationProvider(["Critique output."])
    chat = create_example_refinement_chat(
        example=_target_example(),
        constitution_element=_constitution_element(),
        examples=[_few_shot_example()],
        provider=provider,
    )

    message = chat.get_critique()

    assert message.role == "assistant"
    assert message.content == "Critique output."
    assert chat.conversation() == [message]


def test_get_response_returns_response_with_critique_context() -> None:
    provider = FakeConversationProvider(["Critique output.", "Response output."])
    chat = create_example_refinement_chat(
        example=_target_example(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
    )

    chat.get_critique()
    message = chat.get_response()

    assert message.role == "assistant"
    assert message.content == (
        "Using Critique:\nCritique output.\n\nObtained response:\nResponse output."
    )


def test_get_response_uses_updated_critique() -> None:
    provider = FakeConversationProvider(["Critique output.", "Response output."])
    chat = create_example_refinement_chat(
        example=_target_example(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
    )

    chat.get_critique()
    chat.update_critique("Updated critique.")
    message = chat.get_response()

    assert message.content == (
        "Using Critique:\nUpdated critique.\n\nObtained response:\nResponse output."
    )
    assert provider.calls[-1].messages[1].content == "Updated critique."


def test_message_sends_full_refinement_chat() -> None:
    provider = FakeConversationProvider(
        ["Critique output.", "Response output.", "Discussion output."]
    )
    chat = create_example_refinement_chat(
        example=_target_example(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
        model="test-model",
    )

    chat.get_critique()
    chat.get_response()
    message = chat.message("How should I improve the example?")

    assert message.content == "Discussion output."
    assert provider.calls[-1].model == "test-model"
    assert [message.content for message in provider.calls[-1].messages] == [
        "Critique output.",
        "Using Critique:\nCritique output.\n\nObtained response:\nResponse output.",
        "How should I improve the example?",
    ]


def test_update_critique_updates_visible_chat_and_clears_stale_response() -> None:
    provider = FakeConversationProvider(["Critique output.", "Response output."])
    chat = create_example_refinement_chat(
        example=_target_example(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=provider,
    )
    chat.get_critique()
    chat.get_response()

    message = chat.update_critique("Updated critique.")

    assert message.content == "Updated critique."
    assert [message.content for message in chat.conversation()] == ["Updated critique."]


def test_update_critique_before_get_critique_raises() -> None:
    chat = create_example_refinement_chat(
        example=_target_example(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=FakeConversationProvider([]),
    )

    with pytest.raises(RuntimeError, match="before generating one"):
        chat.update_critique("Updated critique.")


def test_create_example_refinement_chat_returns_refinement_chat() -> None:
    chat = create_example_refinement_chat(
        example=_target_example(),
        constitution_element=_constitution_element(),
        examples=[],
        provider=FakeConversationProvider([]),
    )

    assert isinstance(chat, ExampleRefinementChat)


def _constitution_element() -> ConstitutionElement:
    return ConstitutionElement(
        constitution_hash="constitution-1",
        critique_prompt="Critique the assistant.",
        response_prompt="Improve the response.",
        example_hashes=["example-1"],
    )


def _target_example() -> ExampleElement:
    return ExampleElement(
        example_hash="target-example",
        user="Target user.",
        bot="Target bot.",
        critique="Target critique.",
        response="Target response.",
    )


def _few_shot_example() -> ExampleElement:
    return ExampleElement(
        example_hash="example-1",
        user="Example user.",
        bot="Example bot.",
        critique="Example critique.",
        response="Example response.",
    )
