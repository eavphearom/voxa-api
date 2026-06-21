from abc import ABC, abstractmethod
from typing import Any

from app.DTO.folder_dtos import FolderCreateDTO, FolderUpdateDTO


class FolderService(ABC):
    @abstractmethod
    def create(self, user_id: int, dto: FolderCreateDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list(self, user_id: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_detail(self, folder_id: int, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update(self, folder_id: int, user_id: int, dto: FolderUpdateDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, folder_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def remove_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_meetings(self, folder_id: int, user_id: int) -> list[dict[str, Any]]:
        raise NotImplementedError
