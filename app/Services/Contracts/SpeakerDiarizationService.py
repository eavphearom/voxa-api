from abc import ABC, abstractmethod

from app.DTO.MeetingTranscriptionDTO import SpeakerTurnDTO


class SpeakerDiarizationService(ABC):
    @abstractmethod
    def diarize(self, file_path: str) -> list[SpeakerTurnDTO]:
        raise NotImplementedError
