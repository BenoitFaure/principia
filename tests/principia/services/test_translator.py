from principia.services.translator import MISSING_TRANSLATION, Translator, translator


def test_translate_returns_requested_language_value() -> None:
    assert translator.translate("navigation.language", "fr") == "Langue"


def test_translate_returns_english_value() -> None:
    assert translator.translate("navigation.language", "en") == "Language"


def test_translate_falls_back_to_english_when_language_key_is_missing() -> None:
    assert translator.translate("translator.english_only", "fr") == "English only"


def test_translate_falls_back_to_english_when_language_is_unknown() -> None:
    assert translator.translate("navigation.language", "es") == "Language"


def test_translate_returns_missing_code_when_key_is_not_in_english() -> None:
    assert translator.translate("missing.element", "fr") == MISSING_TRANSLATION


def test_available_languages_returns_loaded_json_language_codes() -> None:
    assert translator.available_languages() == ("en", "fr")


def test_translate_returns_missing_code_when_english_is_not_loaded() -> None:
    custom_translator = Translator({"fr": {"navigation.language": "Langue"}})

    assert custom_translator.translate("missing.element", "fr") == MISSING_TRANSLATION
