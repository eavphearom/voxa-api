from __future__ import annotations

from typing import Dict

from abc import ABC, abstractmethod
from typing import Any

from app.DTO.LoginDTO import LoginDTO
from app.DTO.GoogleLoginDTO import GoogleLoginDTO
from app.DTO.RegisterDTO import RegisterDTO


class AuthService(ABC):
    @abstractmethod
    def register(self, dto: RegisterDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def login(self, dto: LoginDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def google_login(self, dto: GoogleLoginDTO) -> Dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def logout(self, request) -> bool:
        raise NotImplementedError
