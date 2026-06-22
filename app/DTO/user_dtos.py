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
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None
    profile_file: object | None = None

    @classmethod
    def from_data(cls, data, files=None) -> "UserUpdateDTO":
        files = files or {}
        return cls(
            name=str(data["name"]).strip() if "name" in data and data["name"] is not None else None,
            email=str(data["email"]).strip() if "email" in data and data["email"] is not None else None,
            phone=str(data["phone"]).strip() if "phone" in data and data["phone"] is not None else None,
            avatar=str(data["avatar"]).strip() if "avatar" in data and data["avatar"] is not None else None,
            profile_file=files.get("profile") or files.get("avatar"),
        )


@dataclass(frozen=True, slots=True)
class UserResponseDTO(BaseDTO):
    id: int
    google_id: str | None
    name: str
    email: str
    avatar: str
    role: str
