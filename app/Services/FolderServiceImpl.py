from typing import List, Dict, Any

from app.DTO.folder_dtos import FolderCreateDTO, FolderUpdateDTO
from app.Exceptions import NotFoundException, ValidationException
from app.Repositories.Contracts.FolderRepository import FolderRepository
from app.Repositories.Contracts.MeetingRepository import MeetingRepository
from app.Services.Contracts.FolderService import FolderService


class FolderServiceImpl(FolderService):
    def __init__(self, folder_repository: FolderRepository, meeting_repository: MeetingRepository) -> None:
        self.folder_repository = folder_repository
        self.meeting_repository = meeting_repository

    def create(self, user_id: int, dto: FolderCreateDTO) -> dict[str, Any]:
        self._validate_name(dto.name)
        return self._folder_to_dict(self.folder_repository.create_for_user(user_id, dto.name))

    def list(self, user_id: int) -> List[Dict[str, Any]]:
        return [self._folder_to_dict(folder) for folder in self.folder_repository.list_by_user(user_id)]

    def get_detail(self, folder_id: int, user_id: int) -> dict[str, Any]:
        folder = self._get_owned_folder(folder_id, user_id)
        return {
            **self._folder_to_dict(folder),
            "meetings": self.list_meetings(folder.id, user_id),
        }

    def update(self, folder_id: int, user_id: int, dto: FolderUpdateDTO) -> dict[str, Any]:
        self._validate_name(dto.name)
        folder = self.folder_repository.update_for_user(folder_id, user_id, dto.name)
        if folder is None:
            raise NotFoundException("Folder not found")
        return self._folder_to_dict(folder)

    def delete(self, folder_id: int, user_id: int) -> bool:
        if not self.folder_repository.soft_delete(folder_id, user_id):
            raise NotFoundException("Folder not found")
        return True

    def add_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> dict[str, Any]:
        self._get_owned_folder(folder_id, user_id)
        meeting = self.meeting_repository.find_by_id_for_user(meeting_id, user_id)
        if meeting is None:
            raise NotFoundException("Meeting not found")
        self.folder_repository.add_meeting(folder_id, meeting_id, user_id)
        return self._meeting_to_dict(meeting)

    def remove_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> bool:
        self._get_owned_folder(folder_id, user_id)
        if not self.folder_repository.remove_meeting(folder_id, meeting_id, user_id):
            raise NotFoundException("Meeting is not in this folder")
        return True

    def list_meetings(self, folder_id: int, user_id: int) -> List[Dict[str, Any]]:
        self._get_owned_folder(folder_id, user_id)
        return [self._meeting_to_dict(meeting) for meeting in self.folder_repository.list_meetings(folder_id)]

    def _get_owned_folder(self, folder_id: int, user_id: int):
        folder = self.folder_repository.find_by_id_for_user(folder_id, user_id)
        if folder is None:
            raise NotFoundException("Folder not found")
        return folder

    def _validate_name(self, name: str) -> None:
        if not name:
            raise ValidationException("Folder name is required")
        if len(name) > 255:
            raise ValidationException("Folder name must not exceed 255 characters")

    def _folder_to_dict(self, folder) -> dict[str, Any]:
        return {"id": folder.id, "name": folder.name, "user_id": folder.user_id}

    def _meeting_to_dict(self, meeting) -> dict[str, Any]:
        return {
            "id": meeting.id,
            "title": meeting.title,
            "status": meeting.status,
            "source_type": meeting.source_type,
            "created_at": meeting.created_at,
        }
