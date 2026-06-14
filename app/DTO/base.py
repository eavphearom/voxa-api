from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class BaseDTO:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
