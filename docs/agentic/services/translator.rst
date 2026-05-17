Translator Service
==================

Frontend display text is stored in JSON files under
``src/principia/services/i18n/``. The current language files are
``en.json`` and ``fr.json``.

Use ``principia.services.translator.translator`` to resolve text keys:

.. code-block:: python

   from principia.services.translator import translator

   text = translator.translate("navigation.language", "fr")

``Translator.translate(element, language)`` returns the requested language
value when present. If the element is missing from that language, it falls
back to English. If English also does not define the element, it returns
``4XD2``.

``Translator.available_languages()`` returns the loaded JSON language codes.

The translator does not read NiceGUI storage directly. NiceGUI pages and
components should read the user's language from ``app.storage.user`` and pass
that explicit language code to ``translate``.
