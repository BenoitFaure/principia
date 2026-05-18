Technology Stack
================

Principia is built on the following external libraries.

Runtime
-------

`NiceGUI <https://nicegui.io/>`_
   Python-first UI framework that renders pages in the browser. Principia uses
   NiceGUI for all frontend pages and components. Pages are registered before
   ``ui.run()`` is called in ``principia.main``.

`FastAPI <https://fastapi.tiangolo.com/>`_
   Async REST framework. The Principia API router is mounted under ``/api``
   inside the NiceGUI application, so both the UI and the API share one server
   process.

`OpenAI SDK <https://github.com/openai/openai-python>`_
   Python client for OpenAI-compatible chat APIs. Used by the prompt test chat
   and example refinement chat to drive the LLM conversation steps.

`Pydantic / pydantic-settings <https://docs.pydantic.dev/>`_
   Data validation and settings management. Request and response bodies in the
   API are Pydantic models; application settings are loaded via
   ``pydantic-settings``.

Tooling
-------

`uv <https://docs.astral.sh/uv/>`_
   Fast Python package manager. Use ``uv sync --all-groups`` to install all
   dependencies including dev and docs extras.

`Ruff <https://docs.astral.sh/ruff/>`_
   Linter and formatter. Configured in ``pyproject.toml`` to check rules
   ``E``, ``F``, ``I``, and ``UP``.

`Pyright <https://github.com/microsoft/pyright>`_
   Static type checker. Covers the ``src/`` tree; run with ``uv run pyright``.

`Sphinx <https://www.sphinx-doc.org/>`_ + `Furo <https://pradyunsg.me/furo/>`_
   Documentation builder (this site). Source files live in ``docs/``; build
   with ``uv run sphinx-build docs docs/_build/html``.
