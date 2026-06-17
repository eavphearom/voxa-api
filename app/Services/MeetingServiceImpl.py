from typing import Any

from app.DTO.MeetingDTO import MeetingDTO
from app.Exceptions import NotFoundException
from app.Repositories.Contracts.MeetingRepository import MeetingRepository
from app.Services.Contracts.MeetingService import MeetingService


class MeetingServiceImpl(MeetingService):
    def __init__(self, repository: MeetingRepository) -> None:
        self.repository = repository

    def get_all(self) -> list[dict[str, Any]]:
        return [self._to_dict(item) for item in self.repository.get_all()]

    def get_by_id(self, object_id: int) -> dict[str, Any]:
        instance = self.repository.get_by_id(object_id)
        if instance is None:
            raise NotFoundException("Meeting not found")
        return self._to_dict(instance)

    def create(self, dto: MeetingDTO) -> dict[str, Any]:
        return self._to_dict(self.repository.create(dto.to_dict()))

    def update(self, object_id: int, dto: MeetingDTO) -> dict[str, Any]:
        instance = self.repository.update(object_id, dto.to_dict())
        if instance is None:
            raise NotFoundException("Meeting not found")
        return self._to_dict(instance)

    def delete(self, object_id: int) -> bool:
        deleted = self.repository.delete(object_id)
        if not deleted:
            raise NotFoundException("Meeting not found")
        return True

    def _to_dict(self, instance) -> dict[str, Any]:
        return {
            "id": instance.id,
            "name": instance.name,
            "created_at": instance.created_at,
            "updated_at": instance.updated_at,
        }
