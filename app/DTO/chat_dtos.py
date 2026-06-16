from dataclasses import dataclass

from app.DTO.base import BaseDTO
from app.Enums import ChatRole


@dataclass(frozen=True, slots=True)
class ChatSessionCreateDTO(BaseDTO):
    meeting_id: int
    user_id: int
    title: str


@dataclass(frozen=True, slots=True)
class ChatSessionUpdateDTO(BaseDTO):
    title: str | None = None


@dataclass(frozen=True, slots=True)
class ChatSessionResponseDTO(BaseDTO):
    id: int
    meeting_id: int
    user_id: int
    title: str
