from abc import ABC, abstractmethod
from typing import Any


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, object_id: int):
        raise NotImplementedError

    @abstractmethod
    def create(self, data: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    def update(self, object_id: int, data: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    def delete(self, object_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def paginate(self, page: int = 1, per_page: int = 10):
        raise NotImplementedError
