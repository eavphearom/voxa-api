from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.DTO.MeetingDTO import MeetingImportDTO, MeetingRecordStartDTO
from app.DTO.meeting_dtos import MeetingListFilterDTO


class MeetingService(ABC):
    @abstractmethod
    def import_meeting(self, user_id: int, dto: MeetingImportDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def start_recording(self, user_id: int, dto: MeetingRecordStartDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def transcribe_recording_chunk(self, meeting_id: int, user_id: int, chunk) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def finish_recording(self, meeting_id: int, user_id: int, source_file) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def list(
        self,
        user_id: int,
        filters: Optional[MeetingListFilterDTO] = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_detail(self, meeting_id: int, user_id: int) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, meeting_id: int, user_id: int) -> bool:
        raise NotImplementedError
