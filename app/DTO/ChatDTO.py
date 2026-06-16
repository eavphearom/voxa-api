from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ChatCreateDTO:
    title: str

    @classmethod
    def from_request(cls, data) -> "ChatCreateDTO":
        return cls(title=str(data.get("title", "New Chat")).strip() or "New Chat")


@dataclass(frozen=True, slots=True)
class ChatUpdateDTO:
    title: str

    @classmethod
    def from_request(cls, data) -> "ChatUpdateDTO":
        return cls(title=str(data.get("title", "")).strip())


@dataclass(frozen=True, slots=True)
class ChatMessageCreateDTO:
    message: str

    @classmethod
    def from_request(cls, data) -> "ChatMessageCreateDTO":
        return cls(message=str(data.get("message", "")).strip())
