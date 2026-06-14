from abc import ABC, abstractmethod

from app.model import User


class UserRepository(ABC):
    @abstractmethod
    def find_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_phone(self, phone: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError
