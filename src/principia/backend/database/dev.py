from pathlib import Path

from pydantic import BaseModel

from .workspace_json_file import WorkspaceJsonFile


class DevElement(BaseModel):
    user: str
    bot: str


class DevFile(WorkspaceJsonFile[DevElement]):
    def __init__(self, workspace_root: Path | None = None) -> None:
        super().__init__(
            subfolder="supervised",
            filename="dev.json",
            model_type=DevElement,
            workspace_root=workspace_root,
        )

    def read(self) -> list[DevElement]:
        return self._read()
