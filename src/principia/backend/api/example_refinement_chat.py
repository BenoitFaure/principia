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
    example: ExampleElement
    constitution_element: ConstitutionElement
    examples: list[ExampleElement]
    model: str = "gpt-4o-mini"


class ChatMessageInput(BaseModel):
    content: str


class CritiqueUpdateInput(BaseModel):
    critique: str


def get_example_refinement_chat_provider() -> ConversationProvider:
    return openai_provider


@router.post("/init")
def init_example_refinement_chat(
    chat_input: ExampleRefinementChatInit,
    provider: Annotated[
        ConversationProvider, Depends(get_example_refinement_chat_provider)
    ],
) -> list[ConversationMessage]:
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
    return example_refinement_chat_state.get().conversation()


@router.post("/critique")
def get_example_refinement_critique() -> ConversationMessage:
    return example_refinement_chat_state.get().get_critique()


@router.put("/critique")
def update_example_refinement_critique(
    critique_input: CritiqueUpdateInput,
) -> ConversationMessage:
    chat = example_refinement_chat_state.get()
    try:
        return chat.update_critique(critique_input.critique)
    except RuntimeError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.post("/response")
def get_example_refinement_response() -> ConversationMessage:
    return example_refinement_chat_state.get().get_response()


@router.post("/message")
def send_example_refinement_message(
    message_input: ChatMessageInput,
) -> ConversationMessage:
    return example_refinement_chat_state.get().message(message_input.content)


@router.delete("")
def kill_example_refinement_chat() -> dict[str, str]:
    example_refinement_chat_state.kill()
    return {"status": "deleted"}
