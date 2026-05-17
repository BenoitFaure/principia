"""NiceGUI user language storage helpers."""

from __future__ import annotations

from nicegui import app

from principia.services.translator import FALLBACK_LANGUAGE, translator

LANGUAGE_STORAGE_KEY = "language"


def get_user_language() -> str:
    """Return the user's stored language, defaulting to English."""
    language = app.storage.user.get(LANGUAGE_STORAGE_KEY, FALLBACK_LANGUAGE)
    if isinstance(language, str) and language in translator.available_languages():
        return language

    app.storage.user[LANGUAGE_STORAGE_KEY] = FALLBACK_LANGUAGE
    return FALLBACK_LANGUAGE


def set_user_language(language: str) -> None:
    """Persist the user's language choice in NiceGUI user storage."""
    if language in translator.available_languages():
        app.storage.user[LANGUAGE_STORAGE_KEY] = language
