from app.Exceptions import ApplicationException
from app.Services.Contracts.MeetingJobService import MeetingJobService


class MeetingJobServiceImpl(MeetingJobService):
    def enqueue(self, meeting_id: int, user_id: int) -> str:
        from app.tasks import process_meeting_transcription

        try:
            task = process_meeting_transcription.delay(meeting_id, user_id)
        except Exception as exc:
            raise ApplicationException("Unable to queue meeting transcription") from exc
        return task.id
