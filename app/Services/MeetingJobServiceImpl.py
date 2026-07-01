import logging

from app.Exceptions import ApplicationException
from app.Services.Contracts.MeetingJobService import MeetingJobService

logger = logging.getLogger(__name__)


class MeetingJobServiceImpl(MeetingJobService):

    def enqueue(self, meeting_id: int, user_id: int) -> str:
        from app.tasks import process_meeting_transcription

        try:
            logger.info("BEFORE DELAY")

            task = process_meeting_transcription.delay(meeting_id, user_id)

            logger.info(f"TASK ID: {task.id}")

        except Exception as exc:
            logger.exception(f"QUEUE ERROR: {exc}")
            raise ApplicationException(
                "Unable to queue meeting transcription"
            ) from exc

        return task.id