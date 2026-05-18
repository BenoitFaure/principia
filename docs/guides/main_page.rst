Main Page
=========

The main page is the starting point for both the SL and RL workflows. It is
split into a toolbar, a left pane, and a right pane.

Toolbar
-------

The toolbar sits in the top-left corner and provides controls that persist
across sessions.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Control
     - Description
   * - **Language**
     - Switch the UI language.
   * - **SL / RL**
     - Navigate back to the main menu or switch between Supervised Learning and
       Reinforcement Learning modes.
   * - **Theme**
     - Toggle between Dark and Light mode.
   * - **OpenAI Key**
     - Set your OpenAI API key. **Required** before using any chat feature.
       Stored persistently in user settings.

.. note::

   To configure the key that signs the session cookie, create a ``.env`` file
   at the project root and set::

      NICEGUI_SECRET=your-secret-here

   Without this, Principia falls back to the default string ``PRINCIPIA_SECRET``,
   which is insecure for any non-local deployment.

Left Pane
---------

.. note:: Currently in development.

The left pane will allow you to generate a full training dataset from your
constitution in a batched manner, without having to run each example manually
through the chat interface.

Right Pane
----------

The right pane displays your **constitution rules**. From here you can:

- **Edit** an existing rule inline.
- **Add** a new rule to the constitution.
- **Click on a Constitution entry** to open the detailed constitution editor,
  where you can manage critique/response examples and run prompt tests against
  that specific rule.
