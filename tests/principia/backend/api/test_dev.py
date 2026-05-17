import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from principia.backend.api.dev import get_dev_file
from principia.backend.api.router import router
from principia.backend.database import DevFile


def create_client(workspace_root: Path) -> TestClient:
    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.dependency_overrides[get_dev_file] = lambda: DevFile(
        workspace_root=workspace_root
    )
    return TestClient(app)


def test_read_dev_returns_elements(tmp_path: Path) -> None:
    dev_file = DevFile(workspace_root=tmp_path)
    elements = [{"user": "User message.", "bot": "Bot message."}]
    dev_file.path.write_text(json.dumps(elements), encoding="utf-8")
    client = create_client(tmp_path)

    response = client.get("/api/supervised/dev")

    assert response.status_code == 200
    assert response.json() == elements


def test_dev_does_not_expose_update_endpoint(tmp_path: Path) -> None:
    client = create_client(tmp_path)

    response = client.put(
        "/api/supervised/dev",
        json={"user": "User message.", "bot": "Bot message."},
    )

    assert response.status_code == 405
