Frontend Layout
===============

The first NiceGUI page is registered at ``/`` from
``principia.frontend.pages.register_pages``. ``src/principia/main.py`` calls
that registration before ``ui.run()``.

Theme choices live in ``src/principia/frontend/theme.py``. Edit the CSS
variables there to change the light green and dark green palettes, shared
spacing, separator styling, and toolbar button states.

The reusable page shell lives in
``src/principia/frontend/components/base_layout.py``. Use
``base_two_pane_layout(language, left_content, right_content)`` for future
pages that need the same screen-sized two-pane workspace. Both panes are
working content areas with no pane contour or background; the vertical line is
their visual separation. The left pane also owns the shared top control strip.

User settings are stored in NiceGUI user storage under ``settings``. Use
``principia.frontend.language.get_user_settings`` and ``save_user_settings``
instead of reading or writing storage directly. The settings modal currently
persists language and OpenAI API key.

Visible frontend labels in the shared layout come from the JSON files in
``src/principia/services/i18n/`` and are resolved through the translator
service. Language selector entries are rendered as uppercase language codes,
such as ``EN`` and ``FR``.
