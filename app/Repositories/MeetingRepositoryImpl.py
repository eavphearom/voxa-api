from app.model import Meeting
from app.Enums.MeetingStatus import MeetingStatus
from app.Repositories.Contracts.MeetingRepository import MeetingRepository


class MeetingRepositoryImpl(MeetingRepository):
    def create_upload(self, data: dict) -> Meeting:
        return Meeting.objects.create(**data)

    def find_by_id_for_user(self, meeting_id: int, user_id: int) -> Meeting | None:
        return Meeting.objects.filter(id=meeting_id, user_id=user_id, is_deleted=False).first()

    def list_by_user(self, user_id: int):
        return Meeting.objects.filter(user_id=user_id, is_deleted=False).order_by("-created_at")

    def update_status(self, meeting_id: int, status: str, user_id: int | None = None) -> Meeting | None:
        meeting = Meeting.objects.filter(id=meeting_id, is_deleted=False).first()
        if meeting is None:
            return None

        meeting.status = status
        meeting.updated_uid = user_id
        meeting.save(update_fields=["status", "updated_uid", "updated_at"])
        return meeting

    def complete_transcription(
        self,
        meeting_id: int,
        language: str | None,
        duration: float | None,
        user_id: int | None = None,
    ) -> Meeting | None:
        meeting = Meeting.objects.filter(id=meeting_id, is_deleted=False).first()
        if meeting is None:
            return None
        meeting.status = MeetingStatus.COMPLETED.value
        meeting.language = language or meeting.language
        if duration is not None:
            meeting.duration = round(duration)
        meeting.updated_uid = user_id
        meeting.save(update_fields=["status", "language", "duration", "updated_uid", "updated_at"])
        return meeting

    def update_recording_file(
        self,
        meeting_id: int,
        file_name: str,
        file_path: str,
        file_size: int,
        user_id: int,
    ) -> Meeting | None:
        meeting = Meeting.objects.filter(id=meeting_id, user_id=user_id, is_deleted=False).first()
        if meeting is None:
            return None
        meeting.file_name = file_name
        meeting.file_path = file_path
        meeting.file_size = file_size
        meeting.status = MeetingStatus.PROCESSING.value
        meeting.updated_uid = user_id
        meeting.save(
            update_fields=["file_name", "file_path", "file_size", "status", "updated_uid", "updated_at"]
        )
        return meeting
