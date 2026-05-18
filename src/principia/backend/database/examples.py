"""Example data model and JSON file accessor."""

from pathlib import Path

from pydantic import BaseModel

from .workspace_json_file import WorkspaceJsonFile


class ExampleElement(BaseModel):
    """A supervised training example with critique and revised response."""

    example_hash: str
    user: str
    bot: str
    critique: str
    response: str


class ExamplesFile(WorkspaceJsonFile[ExampleElement]):
    """Read/write accessor for ``workspace/supervised/examples.json``."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        super().__init__(
            subfolder="supervised",
            filename="examples.json",
            model_type=ExampleElement,
            hash_field="example_hash",
            workspace_root=workspace_root,
        )

    def read(self) -> list[ExampleElement]:
        """Return all stored example elements."""
        return self._read()

    def update(self, element: ExampleElement) -> None:
        """Upsert an example element by hash."""
        self._update(element)

    def delete(self, example_hash: str) -> None:
        """Remove the element with the given hash."""
        self._delete(example_hash)
