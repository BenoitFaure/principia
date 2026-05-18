"""In-memory singleton holder for an active chat instance."""

from fastapi import HTTPException


class ActiveChatState[ChatT]:
    """Hold at most one active chat instance; raise 404 when unset.

    Parameters
    ----------
    not_initialized_detail : str
        Detail string for the 404 response when no chat is active.
    """

    def __init__(self, *, not_initialized_detail: str) -> None:
        self._chat: ChatT | None = None
        self._not_initialized_detail = not_initialized_detail

    def set(self, chat: ChatT) -> ChatT:
        """Replace the active chat and return it."""
        self._chat = chat
        return chat

    def get(self) -> ChatT:
        """Return the active chat, or raise HTTP 404 if none exists."""
        if self._chat is None:
            raise HTTPException(
                status_code=404,
                detail=self._not_initialized_detail,
            )
        return self._chat

    def kill(self) -> None:
        """Clear the active chat."""
        self._chat = None
