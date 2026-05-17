from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from principia.backend.api.examples import get_examples_file
from principia.backend.api.router import router
from principia.backend.database import ExampleElement, ExamplesFile


def create_client(workspace_root: Path) -> TestClient:
    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.dependency_overrides[get_examples_file] = lambda: ExamplesFile(
        workspace_root=workspace_root
    )
    return TestClient(app)


def test_read_examples_returns_elements(tmp_path: Path) -> None:
    examples_file = ExamplesFile(workspace_root=tmp_path)
    element = ExampleElement(
        example_hash="example-1",
        user="User message.",
        bot="Bot message.",
        critique="Critique.",
        response="Response.",
    )
    examples_file.update(element)
    client = create_client(tmp_path)

    response = client.get("/api/supervised/examples")

    assert response.status_code == 200
    assert response.json() == [element.model_dump()]


def test_update_examples_appends_new_element(tmp_path: Path) -> None:
    client = create_client(tmp_path)
    payload = {
        "example_hash": "example-1",
        "user": "User message.",
        "bot": "Bot message.",
        "critique": "Critique.",
        "response": "Response.",
    }

    response = client.put("/api/supervised/examples", json=payload)

    assert response.status_code == 200
    assert response.json() == payload
    assert ExamplesFile(workspace_root=tmp_path).read() == [
        ExampleElement.model_validate(payload)
    ]


def test_update_examples_replaces_matching_hash(tmp_path: Path) -> None:
    examples_file = ExamplesFile(workspace_root=tmp_path)
    examples_file.update(
        ExampleElement(
            example_hash="example-1",
            user="Original user message.",
            bot="Original bot message.",
            critique="Original critique.",
            response="Original response.",
        )
    )
    client = create_client(tmp_path)
    payload = {
        "example_hash": "example-1",
        "user": "Updated user message.",
        "bot": "Updated bot message.",
        "critique": "Updated critique.",
        "response": "Updated response.",
    }

    response = client.put("/api/supervised/examples", json=payload)

    assert response.status_code == 200
    assert ExamplesFile(workspace_root=tmp_path).read() == [
        ExampleElement.model_validate(payload)
    ]
