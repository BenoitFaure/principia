from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from principia.backend.api.constitution import get_constitution_file
from principia.backend.api.router import router
from principia.backend.database import ConstitutionElement, ConstitutionFile


def create_client(workspace_root: Path) -> TestClient:
    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.dependency_overrides[get_constitution_file] = lambda: ConstitutionFile(
        workspace_root=workspace_root
    )
    return TestClient(app)


def test_read_constitution_returns_elements(tmp_path: Path) -> None:
    constitution_file = ConstitutionFile(workspace_root=tmp_path)
    element = ConstitutionElement(
        constitution_hash="constitution-1",
        critique_prompt="Critique this response.",
        response_prompt="Improve this response.",
        example_hashes=["example-1"],
    )
    constitution_file.update(element)
    client = create_client(tmp_path)

    response = client.get("/api/supervised/constitution")

    assert response.status_code == 200
    assert response.json() == [element.model_dump()]


def test_update_constitution_appends_new_element(tmp_path: Path) -> None:
    client = create_client(tmp_path)
    payload = {
        "constitution_hash": "constitution-1",
        "critique_prompt": "Critique this response.",
        "response_prompt": "Improve this response.",
        "example_hashes": ["example-1"],
    }

    response = client.put("/api/supervised/constitution", json=payload)

    assert response.status_code == 200
    assert response.json() == payload
    assert ConstitutionFile(workspace_root=tmp_path).read() == [
        ConstitutionElement.model_validate(payload)
    ]


def test_update_constitution_replaces_matching_hash(tmp_path: Path) -> None:
    constitution_file = ConstitutionFile(workspace_root=tmp_path)
    constitution_file.update(
        ConstitutionElement(
            constitution_hash="constitution-1",
            critique_prompt="Original critique.",
            response_prompt="Original response.",
            example_hashes=["example-1"],
        )
    )
    client = create_client(tmp_path)
    payload = {
        "constitution_hash": "constitution-1",
        "critique_prompt": "Updated critique.",
        "response_prompt": "Updated response.",
        "example_hashes": ["example-2"],
    }

    response = client.put("/api/supervised/constitution", json=payload)

    assert response.status_code == 200
    assert ConstitutionFile(workspace_root=tmp_path).read() == [
        ConstitutionElement.model_validate(payload)
    ]
