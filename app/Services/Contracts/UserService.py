from __future__ import annotations

from typing import Dict

from abc import ABC, abstractmethod
from typing import Any

from app.DTO.user_dtos import UserUpdateDTO


class UserService(ABC):
    @abstractmethod
    def get_profile(self, user_id: int) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def update_profile(self, user_id: int, dto: UserUpdateDTO) -> Dict[str, Any]:
        raise NotImplementedError
