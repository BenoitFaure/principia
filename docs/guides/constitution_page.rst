Constitution Page
=================

Reached by clicking a constitution entry on the main page. Provides a detailed
editor for linking rules to examples and iterating on both with AI assistance.

Layout
------

- **Left pane** — your constitution rules.
- **Right pane** — your examples.

Linking Rules to Examples
--------------------------

1. Click the **selector** next to a rule to select it.
2. In the right pane, tick one or more examples to link to that rule.
3. Press **Save** — links are not persisted until you do.

A rule can be linked to multiple examples, and an example can be linked to
multiple rules.

Creating and Editing Examples
------------------------------

Examples are created and edited the same way as rules. In addition, each
example has **AI assistance** available via the chat panel.

AI Chat Assistance
------------------

With a constitution rule selected, the chat panel lets you generate a
**critique** and a **revised response** for any user/bot dialogue:

1. Select a constitution rule in the left pane.
2. Open or create an example (user message + bot response).
3. Use the chat to ask the AI to critique the bot response against the selected
   rule and propose a revision.
4. Accept or adjust the generated critique and response before saving the
   example.

Model Selection
---------------

A model selector in the chat panel controls which LLM is used for AI
assistance. To add models to the list, edit::

   src/principia/services/openai/model_list.md
