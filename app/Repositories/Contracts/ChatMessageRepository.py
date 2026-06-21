from abc import ABC, abstractmethod

from app.model import ChatMessage
from app.Repositories.BaseRepository import BaseRepository


class ChatMessageRepository(BaseRepository, ABC):
    @abstractmethod
    def create_for_chat(
        self,
        chat_id: int,
        role: str,
        content: str,
        user_id: int | None = None,
    ) -> ChatMessage:
        raise NotImplementedError

    @abstractmethod
    def list_by_chat(self, chat_id: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_id_for_chat(self, message_id: int, chat_id: int) -> ChatMessage | None:
        raise NotImplementedError
