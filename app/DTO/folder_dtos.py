from dataclasses import dataclass

from app.DTO.base import BaseDTO


@dataclass(frozen=True, slots=True)
class FolderCreateDTO(BaseDTO):
    user_id: int
    name: str


@dataclass(frozen=True, slots=True)
class FolderUpdateDTO(BaseDTO):
    name: str | None = None


@dataclass(frozen=True, slots=True)
class FolderResponseDTO(BaseDTO):
    id: int
    user_id: int
    name: str
