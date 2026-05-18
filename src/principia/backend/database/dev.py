"""Dev (red-team) prompt data model and JSON file accessor."""

from pathlib import Path

from pydantic import BaseModel

from .workspace_json_file import WorkspaceJsonFile


class DevElement(BaseModel):
    """A red-team prompt pair used to test constitution rules."""

    user: str
    bot: str


class DevFile(WorkspaceJsonFile[DevElement]):
    """Read-only accessor for ``workspace/supervised/dev.json``."""

    def __init__(self, workspace_root: Path | None = None) -> None:
        super().__init__(
            subfolder="supervised",
            filename="dev.json",
            model_type=DevElement,
            workspace_root=workspace_root,
        )

    def read(self) -> list[DevElement]:
        """Return all stored dev prompt pairs."""
        return self._read()
