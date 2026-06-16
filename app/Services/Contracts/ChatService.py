from abc import ABC, abstractmethod
from typing import Any

from app.DTO.ChatDTO import ChatCreateDTO, ChatMessageCreateDTO, ChatUpdateDTO


class ChatService(ABC):
    @abstractmethod
    def create(self, user_id: int, dto: ChatCreateDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list(self, user_id: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_detail(self, chat_id: int, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update(self, chat_id: int, user_id: int, dto: ChatUpdateDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, chat_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def send_message(self, chat_id: int, user_id: int, dto: ChatMessageCreateDTO) -> dict[str, Any]:
        raise NotImplementedError
