from __future__ import annotations

from typing import Dict

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BaseDTO:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
