from fastapi import FastAPI
from fastapi.testclient import TestClient

from principia.backend.api.example_refinement_chat import (
    example_refinement_chat_state,
    get_example_refinement_chat_provider,
)
from principia.backend.api.prompt_test_chat import (
    get_prompt_test_chat_provider,
    prompt_test_chat_state,
)
from principia.backend.api.router import router
from principia.services.openai_provider import ConversationInput, ConversationOutput


class FakeConversationProvider:
    def __init__(self, responses: list[str]) -> None:
        self._responses = responses
        self.calls: list[ConversationInput] = []

    def conversation(self, conversation_input: ConversationInput) -> ConversationOutput:
        self.calls.append(conversation_input)
        return ConversationOutput(message=self._responses.pop(0))


def create_client(provider: FakeConversationProvider) -> TestClient:
    prompt_test_chat_state.kill()
    example_refinement_chat_state.kill()
    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.dependency_overrides[get_prompt_test_chat_provider] = lambda: provider
    app.dependency_overrides[get_example_refinement_chat_provider] = lambda: provider
    return TestClient(app)


def test_prompt_test_get_before_init_returns_404() -> None:
    client = create_client(FakeConversationProvider([]))

    response = client.get("/api/chat/prompt-test")

    assert response.status_code == 404
    assert response.json()["detail"] == "Prompt test chat is not initialized."


def test_prompt_test_action_before_init_returns_404() -> None:
    client = create_client(FakeConversationProvider([]))

    response = client.post("/api/chat/prompt-test/critique")

    assert response.status_code == 404


def test_prompt_test_init_creates_empty_conversation() -> None:
    client = create_client(FakeConversationProvider([]))

    response = client.post("/api/chat/prompt-test/init", json=_prompt_test_payload())

    assert response.status_code == 200
    assert response.json() == []


def test_prompt_test_init_replaces_previous_chat() -> None:
    client = create_client(FakeConversationProvider(["Critique output."]))
    client.post("/api/chat/prompt-test/init", json=_prompt_test_payload())
    client.post("/api/chat/prompt-test/critique")

    response = client.post("/api/chat/prompt-test/init", json=_prompt_test_payload())

    assert response.status_code == 200
    assert client.get("/api/chat/prompt-test").json() == []


def test_prompt_test_critique_response_update_and_step() -> None:
    provider = FakeConversationProvider(
        ["Critique output.", "Response output.", "Second response output."]
    )
    client = create_client(provider)
    client.post("/api/chat/prompt-test/init", json=_prompt_test_payload())

    critique_response = client.post("/api/chat/prompt-test/critique")
    response_response = client.post("/api/chat/prompt-test/response")
    update_response = client.put(
        "/api/chat/prompt-test/critique",
        json={"critique": "Updated critique."},
    )
    step_response = client.post("/api/chat/prompt-test/step")

    assert critique_response.json() == {
        "role": "assistant",
        "content": "Critique output.",
    }
    assert response_response.json() == {
        "role": "assistant",
        "content": "Response output.",
    }
    assert update_response.json() == {
        "role": "assistant",
        "content": "Updated critique.",
    }
    assert step_response.status_code == 200
    assert step_response.json()[-1] == {
        "role": "assistant",
        "content": "Second response output.",
    }


def test_prompt_test_update_critique_before_critique_returns_400() -> None:
    client = create_client(FakeConversationProvider([]))
    client.post("/api/chat/prompt-test/init", json=_prompt_test_payload())

    response = client.put(
        "/api/chat/prompt-test/critique",
        json={"critique": "Updated critique."},
    )

    assert response.status_code == 400


def test_prompt_test_delete_kills_only_prompt_test_chat() -> None:
    provider = FakeConversationProvider([])
    client = create_client(provider)
    client.post("/api/chat/prompt-test/init", json=_prompt_test_payload())
    client.post(
        "/api/chat/example-refinement/init",
        json=_example_refinement_payload(),
    )

    delete_response = client.delete("/api/chat/prompt-test")

    assert delete_response.json() == {"status": "deleted"}
    assert client.get("/api/chat/prompt-test").status_code == 404
    assert client.get("/api/chat/example-refinement").status_code == 200


def _prompt_test_payload() -> dict[str, object]:
    return {
        "dev_element": {"user": "Red team user.", "bot": "Unsafe bot answer."},
        "constitution_element": _constitution_payload(),
        "examples": [_example_payload()],
        "model": "test-model",
    }


def _example_refinement_payload() -> dict[str, object]:
    return {
        "example": _example_payload(),
        "constitution_element": _constitution_payload(),
        "examples": [],
        "model": "test-model",
    }


def _constitution_payload() -> dict[str, object]:
    return {
        "constitution_hash": "constitution-1",
        "critique_prompt": "Critique the assistant.",
        "response_prompt": "Improve the response.",
        "example_hashes": ["example-1"],
    }


def _example_payload() -> dict[str, str]:
    return {
        "example_hash": "example-1",
        "user": "Example user.",
        "bot": "Example bot.",
        "critique": "Example critique.",
        "response": "Example response.",
    }
