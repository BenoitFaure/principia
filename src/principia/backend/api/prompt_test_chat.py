"""FastAPI routes for the active prompt-test chat session."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from principia.backend.chat import PromptTestChat
from principia.backend.chat.prompt_tester import ConversationProvider
from principia.backend.database import ConstitutionElement, DevElement, ExampleElement
from principia.services.openai_provider import ConversationMessage, openai_provider

from .chat_state import ActiveChatState

router = APIRouter(prefix="/chat/prompt-test", tags=["prompt-test-chat"])
prompt_test_chat_state = ActiveChatState[PromptTestChat](
    not_initialized_detail="Prompt test chat is not initialized."
)


class PromptTestChatInit(BaseModel):
    """Request body for initialising a prompt-test chat."""

    dev_element: DevElement
    constitution_element: ConstitutionElement
    examples: list[ExampleElement]
    model: str = "gpt-4o-mini"


class CritiqueUpdateInput(BaseModel):
    """Request body for replacing the current critique text."""

    critique: str


def get_prompt_test_chat_provider() -> ConversationProvider:
    """Dependency: return the global OpenAI provider."""
    return openai_provider


@router.post("/init")
def init_prompt_test_chat(
    chat_input: PromptTestChatInit,
    provider: Annotated[ConversationProvider, Depends(get_prompt_test_chat_provider)],
) -> list[ConversationMessage]:
    """Initialise a new prompt-test chat and return the empty conversation."""
    chat = PromptTestChat(
        dev_element=chat_input.dev_element,
        constitution_element=chat_input.constitution_element,
        examples=chat_input.examples,
        provider=provider,
        model=chat_input.model,
    )
    return prompt_test_chat_state.set(chat).conversation()


@router.get("")
def read_prompt_test_chat() -> list[ConversationMessage]:
    """Return the current conversation history."""
    return prompt_test_chat_state.get().conversation()


@router.post("/critique")
def generate_prompt_test_critique() -> ConversationMessage:
    """Run a critique step and return the generated critique message."""
    critique = prompt_test_chat_state.get().generate_critique()
    return ConversationMessage(role="assistant", content=critique)


@router.put("/critique")
def update_prompt_test_critique(
    critique_input: CritiqueUpdateInput,
) -> ConversationMessage:
    """Replace the current critique text."""
    chat = prompt_test_chat_state.get()
    try:
        chat.update_critique(critique_input.critique)
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return ConversationMessage(role="assistant", content=critique_input.critique)


@router.post("/response")
def generate_prompt_test_response() -> ConversationMessage:
    """Run a response step and return the generated response message."""
    response = prompt_test_chat_state.get().generate_response()
    return ConversationMessage(role="assistant", content=response)


@router.post("/step")
def step_prompt_test_chat() -> list[ConversationMessage]:
    """Advance the conversation by one critique/response step."""
    return prompt_test_chat_state.get().step()


@router.delete("")
def kill_prompt_test_chat() -> dict[str, str]:
    """Delete the active prompt-test chat."""
    prompt_test_chat_state.kill()
    return {"status": "deleted"}
