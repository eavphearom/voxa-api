from abc import ABC, abstractmethod
from typing import Any

from app.DTO.MeetingDTO import MeetingDTO


class MeetingService(ABC):
    @abstractmethod
    def get_all(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, object_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def create(self, dto: MeetingDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update(self, object_id: int, dto: MeetingDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, object_id: int) -> bool:
        raise NotImplementedError
