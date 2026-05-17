"""NiceGUI user settings storage helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from nicegui import app

from principia.services.translator import FALLBACK_LANGUAGE, translator

SETTINGS_STORAGE_KEY = "settings"
LANGUAGE_STORAGE_KEY = "language"
OPENAI_API_KEY_STORAGE_KEY = "openai_api_key"


@dataclass(frozen=True)
class UserSettings:
    """Settings persisted in NiceGUI user storage."""

    language: str = FALLBACK_LANGUAGE
    openai_api_key: str = ""


def get_user_settings() -> UserSettings:
    """Return validated user settings, defaulting missing values."""
    raw_settings = app.storage.user.get(SETTINGS_STORAGE_KEY, {})

    if isinstance(raw_settings, dict):
        language = raw_settings.get(LANGUAGE_STORAGE_KEY, FALLBACK_LANGUAGE)
        openai_api_key = raw_settings.get(OPENAI_API_KEY_STORAGE_KEY, "")
    else:
        language = FALLBACK_LANGUAGE
        openai_api_key = ""

    legacy_language = app.storage.user.get(LANGUAGE_STORAGE_KEY)
    if (
        isinstance(raw_settings, dict)
        and LANGUAGE_STORAGE_KEY not in raw_settings
        and isinstance(legacy_language, str)
    ):
        language = legacy_language

    settings = UserSettings(
        language=_validated_language(language),
        openai_api_key=openai_api_key if isinstance(openai_api_key, str) else "",
    )
    save_user_settings(settings)
    return settings


def save_user_settings(settings: UserSettings) -> None:
    """Persist user settings in NiceGUI user storage."""
    app.storage.user[SETTINGS_STORAGE_KEY] = asdict(
        UserSettings(
            language=_validated_language(settings.language),
            openai_api_key=settings.openai_api_key,
        ),
    )


def get_user_language() -> str:
    """Return the user's stored language, defaulting to English."""
    return get_user_settings().language


def set_user_language(language: str) -> None:
    """Persist the user's language choice in NiceGUI user storage."""
    settings = get_user_settings()
    save_user_settings(
        UserSettings(
            language=language,
            openai_api_key=settings.openai_api_key,
        ),
    )


def _validated_language(language: object) -> str:
    if isinstance(language, str) and language in translator.available_languages():
        return language
    return FALLBACK_LANGUAGE
