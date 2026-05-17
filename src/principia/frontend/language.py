"""NiceGUI user settings storage helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum

from nicegui import app

from principia.services.translator import FALLBACK_LANGUAGE, translator

SETTINGS_STORAGE_KEY = "settings"
LANGUAGE_STORAGE_KEY = "language"
OPENAI_API_KEY_STORAGE_KEY = "openai_api_key"
LEARNING_STAGE_STORAGE_KEY = "learning_stage"
THEME_MODE_STORAGE_KEY = "theme_mode"


class LearningStage(StrEnum):
    """Learning stages available in the main workspace."""

    SUPERVISED = "supervised_learning"
    REINFORCEMENT = "reinforcement_learning"


class ThemeMode(StrEnum):
    """Theme modes available in the main workspace."""

    LIGHT = "light"
    DARK = "dark"


@dataclass(frozen=True)
class UserSettings:
    """Settings persisted in NiceGUI user storage."""

    language: str = FALLBACK_LANGUAGE
    openai_api_key: str = ""
    learning_stage: LearningStage = LearningStage.SUPERVISED
    theme_mode: ThemeMode = ThemeMode.LIGHT


def get_user_settings() -> UserSettings:
    """Return validated user settings, defaulting missing values."""
    raw_settings = app.storage.user.get(SETTINGS_STORAGE_KEY, {})

    if isinstance(raw_settings, dict):
        language = raw_settings.get(LANGUAGE_STORAGE_KEY, FALLBACK_LANGUAGE)
        openai_api_key = raw_settings.get(OPENAI_API_KEY_STORAGE_KEY, "")
        learning_stage = raw_settings.get(
            LEARNING_STAGE_STORAGE_KEY,
            LearningStage.SUPERVISED.value,
        )
        theme_mode = raw_settings.get(THEME_MODE_STORAGE_KEY, ThemeMode.LIGHT.value)
    else:
        language = FALLBACK_LANGUAGE
        openai_api_key = ""
        learning_stage = LearningStage.SUPERVISED.value
        theme_mode = ThemeMode.LIGHT.value

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
        learning_stage=_validated_learning_stage(learning_stage),
        theme_mode=_validated_theme_mode(theme_mode),
    )
    save_user_settings(settings)
    return settings


def save_user_settings(settings: UserSettings) -> None:
    """Persist user settings in NiceGUI user storage."""
    validated_settings = UserSettings(
        language=_validated_language(settings.language),
        openai_api_key=settings.openai_api_key,
        learning_stage=_validated_learning_stage(settings.learning_stage),
        theme_mode=_validated_theme_mode(settings.theme_mode),
    )
    raw_settings = asdict(validated_settings)
    raw_settings[LEARNING_STAGE_STORAGE_KEY] = validated_settings.learning_stage.value
    raw_settings[THEME_MODE_STORAGE_KEY] = validated_settings.theme_mode.value
    app.storage.user[SETTINGS_STORAGE_KEY] = raw_settings


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
            learning_stage=settings.learning_stage,
            theme_mode=settings.theme_mode,
        ),
    )


def get_user_learning_stage() -> LearningStage:
    """Return the user's stored learning stage."""
    return get_user_settings().learning_stage


def set_user_learning_stage(learning_stage: LearningStage) -> None:
    """Persist the user's learning stage choice in NiceGUI user storage."""
    settings = get_user_settings()
    save_user_settings(
        UserSettings(
            language=settings.language,
            openai_api_key=settings.openai_api_key,
            learning_stage=learning_stage,
            theme_mode=settings.theme_mode,
        ),
    )


def get_user_theme_mode() -> ThemeMode:
    """Return the user's stored theme mode."""
    return get_user_settings().theme_mode


def _validated_language(language: object) -> str:
    if isinstance(language, str) and language in translator.available_languages():
        return language
    return FALLBACK_LANGUAGE


def _validated_learning_stage(learning_stage: object) -> LearningStage:
    if isinstance(learning_stage, LearningStage):
        return learning_stage
    if isinstance(learning_stage, str):
        try:
            return LearningStage(learning_stage)
        except ValueError:
            pass
    return LearningStage.SUPERVISED


def _validated_theme_mode(theme_mode: object) -> ThemeMode:
    if isinstance(theme_mode, ThemeMode):
        return theme_mode
    if isinstance(theme_mode, str):
        try:
            return ThemeMode(theme_mode)
        except ValueError:
            pass
    return ThemeMode.LIGHT
