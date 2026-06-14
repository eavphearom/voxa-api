from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginDTO:
    email: str
    password: str
