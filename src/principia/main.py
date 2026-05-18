"""Application entry point: mounts the API router and starts NiceGUI."""

import os

from nicegui import app, ui

from principia.backend.api import router
from principia.frontend.pages import register_pages
from principia.services.translator import FALLBACK_LANGUAGE, translator


def main() -> None:
    """Mount the FastAPI router and start the NiceGUI server."""
    app.include_router(router, prefix="/api")
    register_pages()

    NICEGUI_SECRET = os.environ.get("NICEGUI_SECRET", "PRINCIPIA_SECRET")
    ui.run(
        title=translator.translate("app.title", FALLBACK_LANGUAGE),
        storage_secret=NICEGUI_SECRET,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
