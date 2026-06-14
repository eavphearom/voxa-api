from dataclasses import dataclass

from app.DTO.base import BaseDTO
from app.Enums import Role


@dataclass(frozen=True, slots=True)
class UserCreateDTO(BaseDTO):
    email: str
    name: str
    google_id: str | None = None
    avatar: str = ""
    role: Role = Role.USER


@dataclass(frozen=True, slots=True)
class UserUpdateDTO(BaseDTO):
    name: str | None = None
    avatar: str | None = None
    role: Role | None = None


@dataclass(frozen=True, slots=True)
class UserResponseDTO(BaseDTO):
    id: int
    google_id: str | None
    name: str
    email: str
    avatar: str
    role: str
