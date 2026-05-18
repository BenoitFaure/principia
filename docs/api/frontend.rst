Frontend
========

Package Structure
-----------------

.. code-block:: text

   principia.frontend
   ├── language.py          — user settings helpers (language, theme, learning stage)
   ├── theme.py             — CSS variable injection and theme application
   ├── components/
   │   ├── base_layout.py                            — shared two-pane shell + toolbar
   │   ├── supervised_learning_constitution_edit.py  — constitution edit dialog
   │   └── supervised_learning_example_edit.py       — example edit dialog with AI chat
   └── pages/
       ├── home.py                                   — root page (/)
       ├── supervised_learning_main.py               — SL main workspace (/supervised)
       ├── supervised_learning_constitution_edit.py  — constitution/example linker
       ├── supervised_learning_constitution_test.py  — test page for one rule
       └── reinforcement_learning_main.py            — RL workspace (placeholder)

All pages are registered in ``principia.frontend.pages`` and mounted before
``ui.run()`` is called in ``principia.main``.

User Settings
-------------

.. automodule:: principia.frontend.language
   :members:
   :undoc-members:
   :show-inheritance:

Theme
-----

.. automodule:: principia.frontend.theme
   :members:
   :undoc-members:
   :show-inheritance:

Components
----------

Base Layout
^^^^^^^^^^^

.. automodule:: principia.frontend.components.base_layout
   :members:
   :undoc-members:
   :show-inheritance:

Constitution Edit Dialog
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: principia.frontend.components.supervised_learning_constitution_edit
   :members:
   :undoc-members:
   :show-inheritance:

Example Edit Dialog
^^^^^^^^^^^^^^^^^^^

.. automodule:: principia.frontend.components.supervised_learning_example_edit
   :members:
   :undoc-members:
   :show-inheritance:

Pages
-----

Home
^^^^

.. automodule:: principia.frontend.pages.home
   :members:
   :undoc-members:
   :show-inheritance:

Supervised Learning — Main
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: principia.frontend.pages.supervised_learning_main
   :members:
   :undoc-members:
   :show-inheritance:

Supervised Learning — Constitution Edit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: principia.frontend.pages.supervised_learning_constitution_edit
   :members:
   :undoc-members:
   :show-inheritance:

Supervised Learning — Test
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: principia.frontend.pages.supervised_learning_constitution_test
   :members:
   :undoc-members:
   :show-inheritance:

Reinforcement Learning — Main
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: principia.frontend.pages.reinforcement_learning_main
   :members:
   :undoc-members:
   :show-inheritance:
