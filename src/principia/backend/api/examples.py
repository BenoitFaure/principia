"""FastAPI routes for supervised example CRUD."""

from typing import Annotated

from fastapi import APIRouter, Depends

from principia.backend.database import ExampleElement, ExamplesFile

router = APIRouter(prefix="/supervised/examples", tags=["examples"])


def get_examples_file() -> ExamplesFile:
    """Dependency: return an ``ExamplesFile`` instance."""
    return ExamplesFile()


@router.get("")
def read_examples(
    examples_file: Annotated[ExamplesFile, Depends(get_examples_file)],
) -> list[ExampleElement]:
    """Return all example elements."""
    return examples_file.read()


@router.put("")
def update_examples(
    element: ExampleElement,
    examples_file: Annotated[ExamplesFile, Depends(get_examples_file)],
) -> ExampleElement:
    """Upsert an example element and return it."""
    examples_file.update(element)
    return element


@router.delete("/{example_hash}")
def delete_examples(
    example_hash: str,
    examples_file: Annotated[ExamplesFile, Depends(get_examples_file)],
) -> dict[str, str]:
    """Delete an example element by hash."""
    examples_file.delete(example_hash)
    return {"example_hash": example_hash}
