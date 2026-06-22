from __future__ import annotations

from typing import Dict

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True, slots=True)
class ChatMessageDTO:
    payload: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_request(cls, data) -> "ChatMessageDTO":
        return cls(payload=dict(data))

    def to_dict(self) -> Dict[str, Any]:
        return self.payload
