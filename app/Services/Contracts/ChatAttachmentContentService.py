from abc import ABC, abstractmethod
from typing import Any

from app.DTO.ChatDTO import ChatMessageCreateDTO


class ChatAttachmentContentService(ABC):
    @abstractmethod
    def build_gemini_input(self, dto: ChatMessageCreateDTO) -> tuple[str, list[dict[str, Any]]]:
        raise NotImplementedError
