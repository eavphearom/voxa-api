from dataclasses import dataclass

from app.DTO.ChatMessageAttachmentDTO import ChatMessageAttachmentDTO


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
    attachments: list[ChatMessageAttachmentDTO]

    @classmethod
    def from_request(cls, data, files=None) -> "ChatMessageCreateDTO":
        uploaded_files = []
        if files is not None:
            uploaded_files.extend(files.getlist("attachments"))
            uploaded_files.extend(files.getlist("attachments[]"))

        return cls(
            message=str(data.get("message", "")).strip(),
            attachments=[
                ChatMessageAttachmentDTO.from_uploaded_file(uploaded_file)
                for uploaded_file in uploaded_files
            ],
        )
