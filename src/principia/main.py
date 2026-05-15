# src/principia/main.py
import os

from nicegui import app, ui

from principia.backend.api import router


def main():
    app.include_router(router, prefix="/api")

    NICEGUI_SECRET = os.environ.get("NICEGUI_SECRET", "PRINCIPIA_SECRET")
    ui.run(
        title="Principia",
        storage_secret=NICEGUI_SECRET,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
