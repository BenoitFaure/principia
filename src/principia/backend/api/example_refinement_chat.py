"""FastAPI routes for the active example-refinement chat session."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from principia.backend.chat import ExampleRefinementChat
from principia.backend.chat.prompt_tester import ConversationProvider
from principia.backend.database import ConstitutionElement, ExampleElement
from principia.services.openai_provider import ConversationMessage, openai_provider

from .chat_state import ActiveChatState

router = APIRouter(
    prefix="/chat/example-refinement",
    tags=["example-refinement-chat"],
)
example_refinement_chat_state = ActiveChatState[ExampleRefinementChat](
    not_initialized_detail="Example refinement chat is not initialized."
)


class ExampleRefinementChatInit(BaseModel):
    """Request body for initialising an example-refinement chat."""

    example: ExampleElement
    constitution_element: ConstitutionElement
    examples: list[ExampleElement]
    model: str = "gpt-4o-mini"


class ChatMessageInput(BaseModel):
    """Request body for sending a free-form chat message."""

    content: str


class CritiqueUpdateInput(BaseModel):
    """Request body for replacing the current critique text."""

    critique: str


def get_example_refinement_chat_provider() -> ConversationProvider:
    """Dependency: return the global OpenAI provider."""
    return openai_provider


@router.post("/init")
def init_example_refinement_chat(
    chat_input: ExampleRefinementChatInit,
    provider: Annotated[
        ConversationProvider, Depends(get_example_refinement_chat_provider)
    ],
) -> list[ConversationMessage]:
    """Initialise a new example-refinement chat and return the empty conversation."""
    chat = ExampleRefinementChat(
        example=chat_input.example,
        constitution_element=chat_input.constitution_element,
        examples=chat_input.examples,
        provider=provider,
        model=chat_input.model,
    )
    return example_refinement_chat_state.set(chat).conversation()


@router.get("")
def read_example_refinement_chat() -> list[ConversationMessage]:
    """Return the current conversation history."""
    return example_refinement_chat_state.get().conversation()


@router.post("/critique")
def get_example_refinement_critique() -> ConversationMessage:
    """Generate and return a critique message for the loaded example."""
    return example_refinement_chat_state.get().get_critique()


@router.put("/critique")
def update_example_refinement_critique(
    critique_input: CritiqueUpdateInput,
) -> ConversationMessage:
    """Replace the current critique text."""
    chat = example_refinement_chat_state.get()
    try:
        return chat.update_critique(critique_input.critique)
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/response")
def get_example_refinement_response() -> ConversationMessage:
    """Generate and return a revised response based on the current critique."""
    return example_refinement_chat_state.get().get_response()


@router.post("/message")
def send_example_refinement_message(
    message_input: ChatMessageInput,
) -> ConversationMessage:
    """Send a free-form message and return the assistant reply."""
    return example_refinement_chat_state.get().message(message_input.content)


@router.delete("")
def kill_example_refinement_chat() -> dict[str, str]:
    """Delete the active example-refinement chat."""
    example_refinement_chat_state.kill()
    return {"status": "deleted"}
