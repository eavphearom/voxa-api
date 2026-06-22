from __future__ import annotations

from typing import List

from abc import ABC, abstractmethod

from app.DTO.MeetingTranscriptionDTO import SpeakerTurnDTO


class SpeakerDiarizationService(ABC):
    @abstractmethod
    def diarize(self, file_path: str) -> List[SpeakerTurnDTO]:
        raise NotImplementedError
