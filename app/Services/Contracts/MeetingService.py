from abc import ABC, abstractmethod
from typing import Any

from app.DTO.MeetingDTO import MeetingImportDTO, MeetingRecordStartDTO


class MeetingService(ABC):
    @abstractmethod
    def import_meeting(self, user_id: int, dto: MeetingImportDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def start_recording(self, user_id: int, dto: MeetingRecordStartDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def transcribe_recording_chunk(self, meeting_id: int, user_id: int, chunk) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def finish_recording(self, meeting_id: int, user_id: int, source_file) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list(self, user_id: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_detail(self, meeting_id: int, user_id: int) -> dict[str, Any]:
        raise NotImplementedError
