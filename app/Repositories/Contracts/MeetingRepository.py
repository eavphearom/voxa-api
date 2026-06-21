from abc import ABC, abstractmethod

from app.model import Meeting


class MeetingRepository(ABC):
    @abstractmethod
    def create_upload(self, data: dict) -> Meeting:
        raise NotImplementedError

    @abstractmethod
    def find_by_id_for_user(self, meeting_id: int, user_id: int) -> Meeting | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def update_status(self, meeting_id: int, status: str, user_id: int | None = None) -> Meeting | None:
        raise NotImplementedError

    @abstractmethod
    def complete_transcription(
        self,
        meeting_id: int,
        language: str | None,
        duration: float | None,
        user_id: int | None = None,
    ) -> Meeting | None:
        raise NotImplementedError

    @abstractmethod
    def update_recording_file(
        self,
        meeting_id: int,
        file_name: str,
        file_path: str,
        file_size: int,
        user_id: int,
    ) -> Meeting | None:
        raise NotImplementedError
