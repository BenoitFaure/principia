Backend
===========

The backend exports a single FastAPI router from
``principia.backend.api.router``. The application mounts that router under
``/api``, so every route documented here includes the ``/api`` prefix.

Supervised Data
---------------

The supervised data endpoints read and update JSON-backed data in the
workspace database layer.

.. list-table:: Constitution Endpoints
   :header-rows: 1

   * - Method
     - Path
     - Request Body
     - Response
   * - ``GET``
     - ``/api/supervised/constitution``
     - None
     - ``list[ConstitutionElement]``
   * - ``PUT``
     - ``/api/supervised/constitution``
     - ``ConstitutionElement``
     - ``ConstitutionElement``
   * - ``DELETE``
     - ``/api/supervised/constitution/{constitution_hash}``
     - None
     - ``{"constitution_hash": str}``

.. list-table:: Example Endpoints
   :header-rows: 1

   * - Method
     - Path
     - Request Body
     - Response
   * - ``GET``
     - ``/api/supervised/examples``
     - None
     - ``list[ExampleElement]``
   * - ``PUT``
     - ``/api/supervised/examples``
     - ``ExampleElement``
     - ``ExampleElement``
   * - ``DELETE``
     - ``/api/supervised/examples/{example_hash}``
     - None
     - ``{"example_hash": str}``

.. list-table:: Development Example Endpoints
   :header-rows: 1

   * - Method
     - Path
     - Request Body
     - Response
   * - ``GET``
     - ``/api/supervised/dev``
     - None
     - ``list[DevElement]``

The supervised data models are defined in ``principia.backend.database``:

``ConstitutionElement``
   ``constitution_hash: str``, ``critique_prompt: str``,
   ``response_prompt: str``, and ``example_hashes: list[str]``.

``ExampleElement``
   ``example_hash: str``, ``user: str``, ``bot: str``,
   ``critique: str``, and ``response: str``.

``DevElement``
   ``user: str`` and ``bot: str``.

Prompt Test Chat
----------------

The prompt test chat API manages one active ``PromptTestChat`` instance.
Calling ``POST /api/chat/prompt-test/init`` replaces the previous prompt test
chat, if one exists. Deleting this chat does not affect the example refinement
chat.

.. list-table:: Prompt Test Chat Endpoints
   :header-rows: 1

   * - Method
     - Path
     - Request Body
     - Response
   * - ``POST``
     - ``/api/chat/prompt-test/init``
     - ``PromptTestChatInit``
     - ``list[ConversationMessage]``
   * - ``GET``
     - ``/api/chat/prompt-test``
     - None
     - ``list[ConversationMessage]``
   * - ``POST``
     - ``/api/chat/prompt-test/critique``
     - None
     - ``ConversationMessage``
   * - ``PUT``
     - ``/api/chat/prompt-test/critique``
     - ``CritiqueUpdateInput``
     - ``ConversationMessage``
   * - ``POST``
     - ``/api/chat/prompt-test/response``
     - None
     - ``ConversationMessage``
   * - ``POST``
     - ``/api/chat/prompt-test/step``
     - None
     - ``list[ConversationMessage]``
   * - ``DELETE``
     - ``/api/chat/prompt-test``
     - None
     - ``{"status": "deleted"}``

``PromptTestChatInit`` contains ``dev_element: DevElement``,
``constitution_element: ConstitutionElement``, ``examples: list[ExampleElement]``,
and ``model: str = "gpt-4o-mini"``.

``CritiqueUpdateInput`` contains ``critique: str``.

Example Refinement Chat
-----------------------

The example refinement chat API manages one active ``ExampleRefinementChat``
instance. Calling ``POST /api/chat/example-refinement/init`` replaces the
previous example refinement chat, if one exists. Deleting this chat does not
affect the prompt test chat.

.. list-table:: Example Refinement Chat Endpoints
   :header-rows: 1

   * - Method
     - Path
     - Request Body
     - Response
   * - ``POST``
     - ``/api/chat/example-refinement/init``
     - ``ExampleRefinementChatInit``
     - ``list[ConversationMessage]``
   * - ``GET``
     - ``/api/chat/example-refinement``
     - None
     - ``list[ConversationMessage]``
   * - ``POST``
     - ``/api/chat/example-refinement/critique``
     - None
     - ``ConversationMessage``
   * - ``PUT``
     - ``/api/chat/example-refinement/critique``
     - ``CritiqueUpdateInput``
     - ``ConversationMessage``
   * - ``POST``
     - ``/api/chat/example-refinement/response``
     - None
     - ``ConversationMessage``
   * - ``POST``
     - ``/api/chat/example-refinement/message``
     - ``ChatMessageInput``
     - ``ConversationMessage``
   * - ``DELETE``
     - ``/api/chat/example-refinement``
     - None
     - ``{"status": "deleted"}``

``ExampleRefinementChatInit`` contains ``example: ExampleElement``,
``constitution_element: ConstitutionElement``, ``examples: list[ExampleElement]``,
and ``model: str = "gpt-4o-mini"``.

``ChatMessageInput`` contains ``content: str``.

``CritiqueUpdateInput`` contains ``critique: str``.

Chat API Errors
---------------

Chat action endpoints return ``404`` when their chat type has not been
initialized. Critique update endpoints return ``400`` when the underlying chat
cannot update a critique, for example before one has been generated.

API Modules
-----------

.. automodule:: principia.backend.api.router
   :members:
   :undoc-members:

.. automodule:: principia.backend.api.constitution
   :members:
   :undoc-members:

.. automodule:: principia.backend.api.examples
   :members:
   :undoc-members:

.. automodule:: principia.backend.api.dev
   :members:
   :undoc-members:

.. automodule:: principia.backend.api.prompt_test_chat
   :members:
   :undoc-members:

.. automodule:: principia.backend.api.example_refinement_chat
   :members:
   :undoc-members:

.. automodule:: principia.backend.api.chat_state
   :members:
   :undoc-members:

Database Models
---------------

.. automodule:: principia.backend.database
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: principia.backend.database.constitution
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: principia.backend.database.examples
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: principia.backend.database.dev
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: principia.backend.database.workspace_json_file
   :members:
   :undoc-members:
   :show-inheritance:

Chat Classes
------------

.. automodule:: principia.backend.chat.prompt_tester
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: principia.backend.chat.example_refiner
   :members:
   :undoc-members:
   :show-inheritance:
