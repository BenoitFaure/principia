import json
from pathlib import Path

from pydantic import BaseModel


class WorkspaceJsonFile[ModelT: BaseModel]:
    def __init__(
        self,
        *,
        subfolder: str,
        filename: str,
        model_type: type[ModelT],
        hash_field: str | None = None,
        workspace_root: Path | None = None,
    ) -> None:
        self._model_type = model_type
        self._hash_field = hash_field
        self._workspace_root = workspace_root or self._default_workspace_root()
        self._path = self._workspace_root / subfolder / filename
        self._ensure_file_exists()

    @property
    def path(self) -> Path:
        return self._path

    def _read(self) -> list[ModelT]:
        with self._path.open(encoding="utf-8") as json_file:
            data = json.load(json_file)

        if not isinstance(data, list):
            msg = f"Expected {self._path} to contain a JSON list."
            raise ValueError(msg)

        return [self._model_type.model_validate(item) for item in data]

    def _update(self, element: ModelT) -> None:
        if self._hash_field is None:
            msg = "Updates require a configured hash field."
            raise RuntimeError(msg)

        element_hash = getattr(element, self._hash_field)
        elements = self._read()

        for index, existing_element in enumerate(elements):
            if getattr(existing_element, self._hash_field) == element_hash:
                elements[index] = element
                self._write_all(elements)
                return

        elements.append(element)
        self._write_all(elements)

    def _write_all(self, elements: list[ModelT]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        data = [element.model_dump() for element in elements]
        self._path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def _ensure_file_exists(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            self._path.write_text("[]\n", encoding="utf-8")

    @staticmethod
    def _default_workspace_root() -> Path:
        src_root = next(
            parent
            for parent in Path(__file__).resolve().parents
            if parent.name == "src"
        )
        return src_root.parent / "workspace"
