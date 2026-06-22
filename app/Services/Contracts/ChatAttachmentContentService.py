from __future__ import annotations

from typing import Dict, List, Tuple

from abc import ABC, abstractmethod
from typing import Any

from app.DTO.ChatDTO import ChatMessageCreateDTO


class ChatAttachmentContentService(ABC):
    @abstractmethod
    def build_gemini_input(self, dto: ChatMessageCreateDTO) -> Tuple[str, List[Dict[str, Any]]]:
        raise NotImplementedError
