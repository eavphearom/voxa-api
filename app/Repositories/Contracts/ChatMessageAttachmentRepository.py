from abc import ABC, abstractmethod

from app.model import ChatMessageAttachment
from app.Repositories.BaseRepository import BaseRepository


class ChatMessageAttachmentRepository(BaseRepository, ABC):
    @abstractmethod
    def create_for_message(
        self,
        chat_message_id: int,
        data: dict,
        user_id: int | None = None,
    ) -> ChatMessageAttachment:
        raise NotImplementedError

    @abstractmethod
    def list_by_message(self, chat_message_id: int):
        raise NotImplementedError

    @abstractmethod
    def list_by_messages(self, chat_message_ids: list[int]):
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, attachment_id: int, user_id: int | None = None) -> bool:
        raise NotImplementedError
