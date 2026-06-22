from abc import ABC, abstractmethod

from app.model import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, data: dict) -> User:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_google_id(self, google_id: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_phone(self, phone: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User, data: dict) -> User:
        raise NotImplementedError
