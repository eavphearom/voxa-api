from abc import ABC, abstractmethod

from app.model import Chat


class ChatRepository(ABC):
    @abstractmethod
    def create_for_user(self, user_id: int, title: str) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def create_for_meeting(self, user_id: int, meeting_id: int, title: str, chat_type: str) -> Chat:
        raise NotImplementedError

    @abstractmethod
    def find_by_meeting(self, user_id: int, meeting_id: int, chat_type: str) -> Chat | None:
        raise NotImplementedError

    @abstractmethod
    def list_by_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def find_by_id_for_user(self, chat_id: int, user_id: int) -> Chat | None:
        raise NotImplementedError

    @abstractmethod
    def update_for_user(self, chat_id: int, user_id: int, title: str) -> Chat | None:
        raise NotImplementedError

    @abstractmethod
    def soft_delete(self, chat_id: int, user_id: int) -> bool:
        raise NotImplementedError
