from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GoogleLoginDTO:
    id_token: str
