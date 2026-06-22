from __future__ import annotations

from typing import Dict, List

from abc import ABC, abstractmethod
from typing import Any

from app.DTO.ChatMessageAttachmentDTO import ChatMessageAttachmentDTO


class ChatMessageAttachmentService(ABC):
    @abstractmethod
    def create_many(
        self,
        chat_message_id: int,
        attachments: List[ChatMessageAttachmentDTO],
        user_id: int | None = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def list_by_message(self, chat_message_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def group_by_message_ids(self, chat_message_ids: List[int]) -> Dict[int, List[Dict[str, Any]]]:
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, attachment_id: int, user_id: int | None = None) -> bool:
        raise NotImplementedError
