"""FastAPI route for reading red-team dev prompts."""

from typing import Annotated

from fastapi import APIRouter, Depends

from principia.backend.database import DevElement, DevFile

router = APIRouter(prefix="/supervised/dev", tags=["dev"])


def get_dev_file() -> DevFile:
    """Dependency: return a ``DevFile`` instance."""
    return DevFile()


@router.get("")
def read_dev(
    dev_file: Annotated[DevFile, Depends(get_dev_file)],
) -> list[DevElement]:
    """Return all dev prompt pairs."""
    return dev_file.read()
