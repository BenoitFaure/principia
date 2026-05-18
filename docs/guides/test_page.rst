Test Page
=========

Reached by clicking the **Test** button after selecting a constitution rule.
Lets you validate a rule against red-team prompts before committing it to
training.

Editing the Rule and Examples
------------------------------

The test page shows the selected rule and its linked examples. From here you can:

- Edit the rule text directly.
- Add or remove examples.
- Toggle the selection status of individual examples (selected examples are
  passed as few-shot context to the model).

Red-Team Prompts
----------------

The test page draws its input prompts from a dev file you provide. Place your
red-team prompts in either::

   dev.json

or::

   dev.jsonl

Select the prompts you want to test from the list in the interface.

Running a Test
--------------

With a rule, examples, and at least one dev prompt selected:

1. Choose a **teacher model** from the model selector.
2. Click **Critique** to run a critique step — the model analyses the bot
   response against your rule.
3. Click **Response** to run a response step — the model generates a revised
   response based on the critique.
4. Edit the critique or the rule text and rerun either step to observe the
   effect on the output.

Iterate until the critique/response pair looks correct, then return to the
constitution page to save any rule changes.
