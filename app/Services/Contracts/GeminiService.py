from __future__ import annotations

from typing import Dict, List

from abc import ABC, abstractmethod
from typing import Any


class GeminiService(ABC):
    @abstractmethod
    def generate_response(
        self,
        message: str,
        history: List[Dict[str, Any]] | None = None,
        attachment_parts: List[Dict[str, Any]] | None = None,
    ) -> str:
        raise NotImplementedError
