from abc import ABC, abstractmethod
from typing import Any

from app.DTO.ChatMessageAttachmentDTO import ChatMessageAttachmentDTO


class ChatMessageAttachmentService(ABC):
    @abstractmethod
    def create_many(
        self,
        chat_message_id: int,
        attachments: list[ChatMessageAttachmentDTO],
        user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def list_by_message(self, chat_message_id: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def group_by_message_ids(self, chat_message_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, attachment_id: int, user_id: int | None = None) -> bool:
        raise NotImplementedError
