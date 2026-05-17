# src/principia/main.py
import os

from nicegui import app, ui

from principia.backend.api import router
from principia.frontend.pages import register_pages
from principia.services.translator import FALLBACK_LANGUAGE, translator


def main():
    app.include_router(router, prefix="/api")
    register_pages()

    NICEGUI_SECRET = os.environ.get("NICEGUI_SECRET", "PRINCIPIA_SECRET")
    ui.run(
        title=translator.translate("app.title", FALLBACK_LANGUAGE),
        storage_secret=NICEGUI_SECRET,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
