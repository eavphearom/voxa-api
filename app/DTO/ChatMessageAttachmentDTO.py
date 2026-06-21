from dataclasses import dataclass
from pathlib import Path

from app.Enums.AttachmentType import AttachmentType
from app.Exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class ChatMessageAttachmentDTO:
    uploaded_file: object

    @classmethod
    def from_uploaded_file(cls, uploaded_file) -> "ChatMessageAttachmentDTO":
        if not getattr(uploaded_file, "name", ""):
            raise ValidationException("Attachment file_name is required")
        return cls(uploaded_file=uploaded_file)

    @property
    def file_name(self) -> str:
        return self.uploaded_file.name

    @property
    def file_size(self) -> int:
        return int(getattr(self.uploaded_file, "size", 0) or 0)

    @property
    def content_type(self) -> str:
        return str(getattr(self.uploaded_file, "content_type", "") or "application/octet-stream").lower()

    @property
    def extension(self) -> str:
        return Path(self.file_name).suffix.lower()

    @property
    def attachment_type(self) -> AttachmentType:
        if self.content_type.startswith("image/"):
            return AttachmentType.IMAGE
        if self.content_type.startswith("audio/"):
            return AttachmentType.AUDIO
        if self.content_type.startswith("video/"):
            return AttachmentType.VIDEO
        return AttachmentType.FILE
