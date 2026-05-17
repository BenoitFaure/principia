from typing import Annotated

from fastapi import APIRouter, Depends

from principia.backend.database import ExampleElement, ExamplesFile

router = APIRouter(prefix="/supervised/examples", tags=["examples"])


def get_examples_file() -> ExamplesFile:
    return ExamplesFile()


@router.get("")
def read_examples(
    examples_file: Annotated[ExamplesFile, Depends(get_examples_file)],
) -> list[ExampleElement]:
    return examples_file.read()


@router.put("")
def update_examples(
    element: ExampleElement,
    examples_file: Annotated[ExamplesFile, Depends(get_examples_file)],
) -> ExampleElement:
    examples_file.update(element)
    return element


@router.delete("/{example_hash}")
def delete_examples(
    example_hash: str,
    examples_file: Annotated[ExamplesFile, Depends(get_examples_file)],
) -> dict[str, str]:
    examples_file.delete(example_hash)
    return {"example_hash": example_hash}
