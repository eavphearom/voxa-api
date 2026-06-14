from abc import ABC, abstractmethod
from typing import Any

from app.DTO.LoginDTO import LoginDTO
from app.DTO.RegisterDTO import RegisterDTO


class AuthService(ABC):
    @abstractmethod
    def register(self, dto: RegisterDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def login(self, dto: LoginDTO) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def logout(self, request) -> bool:
        raise NotImplementedError
