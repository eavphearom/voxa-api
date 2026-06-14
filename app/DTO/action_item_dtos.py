from dataclasses import dataclass

from app.DTO.base import BaseDTO
from app.Enums import ActionItemStatus


@dataclass(frozen=True, slots=True)
class ActionItemCreateDTO(BaseDTO):
    meeting_id: int
    content: str
    status: ActionItemStatus = ActionItemStatus.PENDING


@dataclass(frozen=True, slots=True)
class ActionItemUpdateDTO(BaseDTO):
    content: str | None = None
    status: ActionItemStatus | None = None


@dataclass(frozen=True, slots=True)
class ActionItemResponseDTO(BaseDTO):
    id: int
    meeting_id: int
    content: str
    status: str
