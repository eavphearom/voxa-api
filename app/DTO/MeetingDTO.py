from __future__ import annotations

from typing import Dict

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class MeetingDTO:
    payload: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_request(cls, data) -> "MeetingDTO":
        return cls(payload=dict(data))

    def to_dict(self) -> Dict[str, Any]:
        return self.payload


@dataclass(frozen=True, slots=True)
class MeetingImportDTO:
    title: str
    source_file: object
    language: str
    duration: int | None = None

    @classmethod
    def from_request(cls, data, files) -> "MeetingImportDTO":
        source_file = (
            files.get("file")
            or files.get("audio_file")
            or files.get("video_file")
            or files.get("meeting_file")
        )
        title = str(data.get("title", "")).strip()
        if not title and source_file is not None:
            title = source_file.name

        duration = data.get("duration")
        return cls(
            title=title or "Untitled Meeting",
            source_file=source_file,
            language=str(data.get("language", "")).strip(),
            duration=int(duration) if duration not in (None, "") else None,
        )


@dataclass(frozen=True, slots=True)
class MeetingRecordStartDTO:
    title: str
    language: str

    @classmethod
    def from_request(cls, data) -> "MeetingRecordStartDTO":
        return cls(
            title=str(data.get("title", "Recorded Meeting")).strip() or "Recorded Meeting",
            language=str(data.get("language", "")).strip(),
        )
