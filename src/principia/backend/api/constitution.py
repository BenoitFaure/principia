"""FastAPI routes for supervised constitution CRUD."""

from typing import Annotated

from fastapi import APIRouter, Depends

from principia.backend.database import ConstitutionElement, ConstitutionFile

router = APIRouter(prefix="/supervised/constitution", tags=["constitution"])


def get_constitution_file() -> ConstitutionFile:
    """Dependency: return a ``ConstitutionFile`` instance."""
    return ConstitutionFile()


@router.get("")
def read_constitution(
    constitution_file: Annotated[ConstitutionFile, Depends(get_constitution_file)],
) -> list[ConstitutionElement]:
    """Return all constitution elements."""
    return constitution_file.read()


@router.put("")
def update_constitution(
    element: ConstitutionElement,
    constitution_file: Annotated[ConstitutionFile, Depends(get_constitution_file)],
) -> ConstitutionElement:
    """Upsert a constitution element and return it."""
    constitution_file.update(element)
    return element


@router.delete("/{constitution_hash}")
def delete_constitution(
    constitution_hash: str,
    constitution_file: Annotated[ConstitutionFile, Depends(get_constitution_file)],
) -> dict[str, str]:
    """Delete a constitution element by hash."""
    constitution_file.delete(constitution_hash)
    return {"constitution_hash": constitution_hash}
