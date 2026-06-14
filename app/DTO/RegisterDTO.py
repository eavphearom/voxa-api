from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RegisterDTO:
    name: str
    email: str
    phone: str
    password: str
