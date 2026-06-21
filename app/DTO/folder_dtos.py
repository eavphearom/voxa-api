from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FolderCreateDTO:
    name: str

    @classmethod
    def from_request(cls, data) -> "FolderCreateDTO":
        return cls(name=str(data.get("name", "")).strip())


@dataclass(frozen=True, slots=True)
class FolderUpdateDTO:
    name: str

    @classmethod
    def from_request(cls, data) -> "FolderUpdateDTO":
        return cls(name=str(data.get("name", "")).strip())


@dataclass(frozen=True, slots=True)
class FolderResponseDTO:
    id: int
    user_id: int
    name: str
