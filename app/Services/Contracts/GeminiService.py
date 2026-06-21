from abc import ABC, abstractmethod
from typing import Any


class GeminiService(ABC):
    @abstractmethod
    def generate_response(
        self,
        message: str,
        history: list[dict[str, Any]] | None = None,
        attachment_parts: list[dict[str, Any]] | None = None,
    ) -> str:
        raise NotImplementedError
