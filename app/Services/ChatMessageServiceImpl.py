from typing import Any

from app.DTO.ChatMessageDTO import ChatMessageDTO
from app.Exceptions import NotFoundException
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Services.Contracts.ChatMessageService import ChatMessageService


class ChatMessageServiceImpl(ChatMessageService):
    def __init__(self, repository: ChatMessageRepository) -> None:
        self.repository = repository

    def get_all(self) -> list[dict[str, Any]]:
        return [self._to_dict(item) for item in self.repository.get_all()]

    def get_by_id(self, object_id: int) -> dict[str, Any]:
        instance = self.repository.get_by_id(object_id)
        if instance is None:
            raise NotFoundException("ChatMessage not found")
        return self._to_dict(instance)

    def create(self, dto: ChatMessageDTO) -> dict[str, Any]:
        return self._to_dict(self.repository.create(dto.to_dict()))

    def update(self, object_id: int, dto: ChatMessageDTO) -> dict[str, Any]:
        instance = self.repository.update(object_id, dto.to_dict())
        if instance is None:
            raise NotFoundException("ChatMessage not found")
        return self._to_dict(instance)

    def delete(self, object_id: int) -> bool:
        deleted = self.repository.delete(object_id)
        if not deleted:
            raise NotFoundException("ChatMessage not found")
        return True

    def _to_dict(self, instance) -> dict[str, Any]:
        return {
            "id": instance.id,
            "chat_id": instance.chat_id,
            "role": instance.role,
            "content": instance.content,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
