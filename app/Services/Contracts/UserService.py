from abc import ABC, abstractmethod
from typing import Any

from app.DTO.user_dtos import UserUpdateDTO


class UserService(ABC):
    @abstractmethod
    def get_profile(self, user_id: int) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_profile(self, user_id: int, dto: UserUpdateDTO) -> dict[str, Any]:
        raise NotImplementedError
