from dataclasses import dataclass
from decimal import Decimal

from app.DTO.base import BaseDTO
from app.Enums import MeetingStatus


@dataclass(frozen=True, slots=True)
class MeetingListFilterDTO(BaseDTO):
    search: str = ""
    start_date: str = ""
    end_date: str = ""

    @classmethod
    def from_query_params(cls, query_params) -> "MeetingListFilterDTO":
        return cls(
            search=str(query_params.get("search", "")).strip(),
            start_date=str(query_params.get("startDate", "")).strip(),
            end_date=str(query_params.get("endDate", "")).strip(),
        )


@dataclass(frozen=True, slots=True)
class MeetingCreateDTO(BaseDTO):
    user_id: int
    title: str
    description: str = ""
    audio_file: object | None = None
    duration: int = 0
    language: str = ""


@dataclass(frozen=True, slots=True)
class MeetingUpdateDTO(BaseDTO):
    title: str | None = None
    description: str | None = None
    duration: int | None = None
    status: MeetingStatus | None = None
    language: str | None = None


@dataclass(frozen=True, slots=True)
class TranscriptSegmentDTO(BaseDTO):
    speaker: str
    start_time: Decimal
    end_time: Decimal
    content: str


@dataclass(frozen=True, slots=True)
class MeetingResponseDTO(BaseDTO):
    id: int
    user_id: int
    title: str
    description: str
    duration: int
    status: str
    language: str
