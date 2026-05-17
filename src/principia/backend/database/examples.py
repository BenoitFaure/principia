from pathlib import Path

from pydantic import BaseModel

from .workspace_json_file import WorkspaceJsonFile


class ExampleElement(BaseModel):
    example_hash: str
    user: str
    bot: str


class ExamplesFile(WorkspaceJsonFile[ExampleElement]):
    def __init__(self, workspace_root: Path | None = None) -> None:
        super().__init__(
            subfolder="supervised",
            filename="examples.json",
            model_type=ExampleElement,
            hash_field="example_hash",
            workspace_root=workspace_root,
        )

    def read(self) -> list[ExampleElement]:
        return self._read()

    def update(self, element: ExampleElement) -> None:
        self._update(element)

    def delete(self, example_hash: str) -> None:
        self._delete(example_hash)
