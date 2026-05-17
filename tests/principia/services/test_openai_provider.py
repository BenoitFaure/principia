from principia.services.openai_provider import (
    OPENAI_KEY_NOT_SET,
    ConversationInput,
    ConversationMessage,
    OpenAIProvider,
)


class FakeMessage:
    def __init__(self, content: str) -> None:
        self.content = content


class FakeChoice:
    def __init__(self, content: str) -> None:
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, content: str) -> None:
        self.choices = [FakeChoice(content)]


class FakeCompletions:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> FakeResponse:
        self.calls.append(kwargs)
        return FakeResponse("Bot response")


class FakeChat:
    def __init__(self) -> None:
        self.completions = FakeCompletions()


class FakeClient:
    def __init__(self) -> None:
        self.chat = FakeChat()


def test_update_api_key_clears_client_for_blank_key() -> None:
    provider = OpenAIProvider(client_factory=lambda _: FakeClient())
    provider.update_api_key("sk-test")

    provider.update_api_key("  ")

    assert not provider.is_set()


def test_update_api_key_sets_client_for_non_blank_key() -> None:
    captured_keys: list[str] = []

    def client_factory(api_key: str) -> FakeClient:
        captured_keys.append(api_key)
        return FakeClient()

    provider = OpenAIProvider(client_factory=client_factory)

    provider.update_api_key("  sk-test  ")

    assert provider.is_set()
    assert captured_keys == ["sk-test"]


def test_conversation_returns_key_not_set_when_client_is_missing() -> None:
    provider = OpenAIProvider(client_factory=lambda _: FakeClient())

    response = provider.conversation(
        ConversationInput(
            messages=[ConversationMessage(role="user", content="Hello")],
        ),
    )

    assert response.message == OPENAI_KEY_NOT_SET


def test_conversation_returns_openai_response() -> None:
    fake_client = FakeClient()
    provider = OpenAIProvider(client_factory=lambda _: fake_client)
    provider.update_api_key("sk-test")

    response = provider.conversation(
        ConversationInput(
            model="test-model",
            messages=[ConversationMessage(role="user", content="Hello")],
        ),
    )

    assert response.message == "Bot response"
    assert fake_client.chat.completions.calls == [
        {
            "model": "test-model",
            "messages": [{"role": "user", "content": "Hello"}],
        },
    ]
