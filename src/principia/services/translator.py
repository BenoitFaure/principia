"""Translation lookup service for frontend text."""

from __future__ import annotations

import json
from importlib import resources
from typing import Final

FALLBACK_LANGUAGE: Final = "en"
MISSING_TRANSLATION: Final = "4XD2"
_I18N_PACKAGE: Final = "principia.services.i18n"


class Translator:
    """Load JSON translation files and resolve text with English fallback."""

    def __init__(self, translations: dict[str, dict[str, str]] | None = None) -> None:
        if translations is None:
            translations = self._load_translations()
        self._translations = translations

    def translate(self, element: str, language: str) -> str:
        """Return the translated text for an element and language.

        Missing requested-language entries fall back to English. Entries missing
        from English return ``MISSING_TRANSLATION``.
        """
        language_translations = self._translations.get(language, {})
        translated = language_translations.get(element)
        if translated is not None:
            return translated

        english_translations = self._translations.get(FALLBACK_LANGUAGE, {})
        return english_translations.get(element, MISSING_TRANSLATION)

    def available_languages(self) -> tuple[str, ...]:
        """Return the language codes with loaded translation files."""
        return tuple(sorted(self._translations))

    @staticmethod
    def _load_translations() -> dict[str, dict[str, str]]:
        translations: dict[str, dict[str, str]] = {}

        for resource in resources.files(_I18N_PACKAGE).iterdir():
            if not resource.is_file() or resource.name == "__init__.py":
                continue
            if not resource.name.endswith(".json"):
                continue

            language = resource.name.removesuffix(".json")
            with resource.open("r", encoding="utf-8") as file:
                data = json.load(file)

            translations[language] = _validate_translation_data(resource.name, data)

        return translations


def _validate_translation_data(file_name: str, data: object) -> dict[str, str]:
    if not isinstance(data, dict):
        raise ValueError(f"{file_name} must contain a JSON object")

    translations: dict[str, str] = {}
    for element, value in data.items():
        if not isinstance(element, str) or not isinstance(value, str):
            raise ValueError(f"{file_name} must map string elements to string values")
        translations[element] = value

    return translations


translator = Translator()
