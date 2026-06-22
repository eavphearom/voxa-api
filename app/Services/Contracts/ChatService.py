from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from app.DTO.ChatDTO import ChatCreateDTO, ChatMessageCreateDTO, ChatUpdateDTO


class ChatService(ABC):
    @abstractmethod
    def create(self, user_id: int, dto: ChatCreateDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list(self, user_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_detail(self, chat_id: int, user_id: int) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_message_detail(self, chat_id: int, user_id: int, message_id: int) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update(self, chat_id: int, user_id: int, dto: ChatUpdateDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, chat_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def send_message(self, chat_id: int, user_id: int, dto: ChatMessageCreateDTO) -> Dict[str, Any]:
        raise NotImplementedError
