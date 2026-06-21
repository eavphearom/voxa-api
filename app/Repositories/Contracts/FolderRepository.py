from abc import ABC, abstractmethod

from app.model import Folder, FolderMeeting


class FolderRepository(ABC):
    @abstractmethod
    def create_for_user(self, user_id: int, name: str) -> Folder:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_id_for_user(self, folder_id: int, user_id: int) -> Folder | None:
        raise NotImplementedError

    @abstractmethod
    def update_for_user(self, folder_id: int, user_id: int, name: str) -> Folder | None:
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, folder_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> FolderMeeting:
        raise NotImplementedError

    @abstractmethod
    def remove_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def list_meetings(self, folder_id: int):
        raise NotImplementedError
