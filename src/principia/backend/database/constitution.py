"""Constitution data model and JSON file accessor."""

from pathlib import Path

from pydantic import BaseModel

from .workspace_json_file import WorkspaceJsonFile


class ConstitutionElement(BaseModel):
    """A single constitution rule with linked example hashes."""

    constitution_hash: str
    critique_prompt: str
    response_prompt: str
    example_hashes: list[str]


class ConstitutionFile(WorkspaceJsonFile[ConstitutionElement]):
    """Read/write accessor for ``workspace/supervised/constitution.json``."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        super().__init__(
            subfolder="supervised",
            filename="constitution.json",
            model_type=ConstitutionElement,
            hash_field="constitution_hash",
            workspace_root=workspace_root,
        )

    def read(self) -> list[ConstitutionElement]:
        """Return all stored constitution elements."""
        return self._read()

    def update(self, element: ConstitutionElement) -> None:
        """Upsert a constitution element by hash."""
        self._update(element)

    def delete(self, constitution_hash: str) -> None:
        """Remove the element with the given hash."""
        self._delete(constitution_hash)
