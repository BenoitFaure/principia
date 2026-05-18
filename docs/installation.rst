Installation
============

Prerequisites
-------------

- `Git <https://git-scm.com/>`_
- Python 3.12 or higher (only needed for the pip option)

Clone the repository first::

   git clone https://github.com/yourname/principia.git
   cd principia

Option 1 — Dev Container (recommended)
---------------------------------------

The dev container sets up the full environment automatically, including Python,
uv, and all dependencies.

**Prerequisites:** `Docker <https://docs.docker.com/get-docker/>`_ and the
`Dev Containers VS Code extension <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers>`_.

Open the cloned folder in VS Code, then click **Reopen in Container** when
prompted (or open the command palette with ``Ctrl+Shift+P`` and select
*Dev Containers: Reopen in Container*).

The container installs all dependencies automatically via ``uv sync``. This may
take a minute on first build.

Option 2 — uv
--------------

**Prerequisites:** `uv <https://docs.astral.sh/uv/getting-started/installation/>`_
installed on your machine.

.. code-block:: bash

   uv sync --all-groups

Option 3 — pip
---------------

.. code-block:: bash

   pip install -e .

To also install dev and docs dependencies:

.. code-block:: bash

   pip install ".[dev,docs]"

Usage
=====

Running the app
---------------

.. code-block:: bash

   # With uv
   uv run principia

   # With pip install
   principia

This starts Principia and opens it in your browser at ``http://localhost:8080``.

If the app misbehaves, bypass Python path issues with:

.. code-block:: bash

   uv run python -m src.principia.main

Linting and formatting
----------------------

Principia uses `Ruff <https://docs.astral.sh/ruff/>`_ for both linting and
formatting.

.. code-block:: bash

   # Check for lint errors
   uv run ruff check .

   # Fix lint errors automatically
   uv run ruff check . --fix

   # Format code
   uv run ruff format .

   # Check formatting without writing changes
   uv run ruff format . --check

Type checking
-------------

.. code-block:: bash

   uv run pyright

Running tests
-------------

.. code-block:: bash

   uv run pytest

Building the documentation
--------------------------

.. code-block:: bash

   # Install docs dependencies (if using uv)
   uv sync --group docs

   # Build HTML docs
   uv run sphinx-build docs docs/_build/html

   # Serve docs locally
   uv run python -m http.server 8081 --directory docs/_build/html

Then open ``http://localhost:8081`` in your browser.
