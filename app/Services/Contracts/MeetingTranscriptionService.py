from abc import ABC, abstractmethod

from app.DTO.MeetingTranscriptionDTO import MeetingTranscriptionResultDTO


class MeetingTranscriptionService(ABC):
    @abstractmethod
    def transcribe(self, file_path: str, language: str | None = None) -> MeetingTranscriptionResultDTO:
        raise NotImplementedError

    @abstractmethod
    def transcribe_live_chunk(self, file_path: str, language: str | None = None) -> MeetingTranscriptionResultDTO:
        raise NotImplementedError
