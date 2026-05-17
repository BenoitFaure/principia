import json
from pathlib import Path

import pytest

from principia.backend.database import (
    ConstitutionElement,
    ConstitutionFile,
    DevElement,
    DevFile,
    ExampleElement,
    ExamplesFile,
)
from principia.backend.database.workspace_json_file import WorkspaceJsonFile


def test_default_workspace_root_is_next_to_src() -> None:
    expected_root = Path(__file__).resolve().parents[4] / "workspace"

    assert WorkspaceJsonFile._default_workspace_root() == expected_root


def test_files_are_created_as_empty_lists(tmp_path: Path) -> None:
    constitution_file = ConstitutionFile(workspace_root=tmp_path)
    examples_file = ExamplesFile(workspace_root=tmp_path)
    dev_file = DevFile(workspace_root=tmp_path)

    assert constitution_file.path.read_text(encoding="utf-8") == "[]\n"
    assert examples_file.path.read_text(encoding="utf-8") == "[]\n"
    assert dev_file.path.read_text(encoding="utf-8") == "[]\n"


def test_constitution_update_appends_new_element(tmp_path: Path) -> None:
    constitution_file = ConstitutionFile(workspace_root=tmp_path)
    element = ConstitutionElement(
        constitution_hash="constitution-1",
        critique_prompt="Critique this response.",
        response_prompt="Improve this response.",
        example_hashes=["example-1"],
    )

    constitution_file.update(element)

    assert constitution_file.read() == [element]


def test_constitution_update_replaces_matching_hash(tmp_path: Path) -> None:
    constitution_file = ConstitutionFile(workspace_root=tmp_path)
    original = ConstitutionElement(
        constitution_hash="constitution-1",
        critique_prompt="Original critique.",
        response_prompt="Original response.",
        example_hashes=["example-1"],
    )
    updated = ConstitutionElement(
        constitution_hash="constitution-1",
        critique_prompt="Updated critique.",
        response_prompt="Updated response.",
        example_hashes=["example-2"],
    )

    constitution_file.update(original)
    constitution_file.update(updated)

    assert constitution_file.read() == [updated]


def test_examples_update_uses_example_hash(tmp_path: Path) -> None:
    examples_file = ExamplesFile(workspace_root=tmp_path)
    original = ExampleElement(
        example_hash="example-1",
        user="User message.",
        bot="Bot message.",
        critique="Original critique.",
        response="Original response.",
    )
    updated = ExampleElement(
        example_hash="example-1",
        user="Updated user message.",
        bot="Updated bot message.",
        critique="Updated critique.",
        response="Updated response.",
    )

    examples_file.update(original)
    examples_file.update(updated)

    assert examples_file.read() == [updated]


def test_dev_file_reads_elements_without_public_update(tmp_path: Path) -> None:
    dev_file = DevFile(workspace_root=tmp_path)
    raw_elements = [{"user": "User message.", "bot": "Bot message."}]
    dev_file.path.write_text(json.dumps(raw_elements), encoding="utf-8")

    assert dev_file.read() == [DevElement(user="User message.", bot="Bot message.")]
    assert not hasattr(dev_file, "update")


def test_read_rejects_non_list_json(tmp_path: Path) -> None:
    constitution_file = ConstitutionFile(workspace_root=tmp_path)
    constitution_file.path.write_text("{}\n", encoding="utf-8")

    with pytest.raises(ValueError, match="contain a JSON list"):
        constitution_file.read()
