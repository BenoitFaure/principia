from fastapi import HTTPException


class ActiveChatState[ChatT]:
    def __init__(self, *, not_initialized_detail: str) -> None:
        self._chat: ChatT | None = None
        self._not_initialized_detail = not_initialized_detail

    def set(self, chat: ChatT) -> ChatT:
        self._chat = chat
        return chat

    def get(self) -> ChatT:
        if self._chat is None:
            raise HTTPException(
                status_code=404,
                detail=self._not_initialized_detail,
            )
        return self._chat

    def kill(self) -> None:
        self._chat = None
