from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List, Dict
from app.DTO.folder_dtos import FolderCreateDTO, FolderUpdateDTO


class FolderService(ABC):
    @abstractmethod
    def create(self, user_id: int, dto: FolderCreateDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list(self, user_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_detail(self, folder_id: int, user_id: int) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update(self, folder_id: int, user_id: int, dto: FolderUpdateDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, folder_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def remove_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_meetings(self, folder_id: int, user_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError
