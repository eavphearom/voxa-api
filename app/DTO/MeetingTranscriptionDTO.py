from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TranscriptionSegmentDTO:
    start: float
    end: float
    text: str


@dataclass(frozen=True, slots=True)
class SpeakerTurnDTO:
    start: float
    end: float
    speaker: str


@dataclass(frozen=True, slots=True)
class MeetingTranscriptionResultDTO:
    text: str
    language: str | None
    duration: float | None
    segments: list[TranscriptionSegmentDTO]
