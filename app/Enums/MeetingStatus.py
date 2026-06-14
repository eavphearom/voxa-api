from enum import StrEnum


class MeetingStatus(StrEnum):
    UPLOADED = "uploaded"
    TRANSCRIBING = "transcribing"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"
