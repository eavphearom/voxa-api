import logging

from django.core.files.storage import default_storage

from app.Enums.ChatRole import ChatRole
from app.Enums.ChatType import ChatType
from app.Enums.MeetingStatus import MeetingStatus
from app.Exceptions import ApplicationException, NotFoundException
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Repositories.Contracts.ChatRepository import ChatRepository
from app.Repositories.Contracts.MeetingRepository import MeetingRepository
from app.Services.Contracts.MeetingProcessingService import MeetingProcessingService
from app.Services.Contracts.MeetingTranscriptionService import MeetingTranscriptionService


logger = logging.getLogger(__name__)


class MeetingProcessingServiceImpl(MeetingProcessingService):
    def __init__(
        self,
        meeting_repository: MeetingRepository,
        chat_repository: ChatRepository,
        message_repository: ChatMessageRepository,
        transcription_service: MeetingTranscriptionService,
    ) -> None:
        self.meeting_repository = meeting_repository
        self.chat_repository = chat_repository
        self.message_repository = message_repository
        self.transcription_service = transcription_service

    def process(self, meeting_id: int, user_id: int) -> None:
        meeting = self.meeting_repository.find_by_id_for_user(meeting_id, user_id)
        if meeting is None:
            raise NotFoundException("Meeting not found")
        meeting_chat = self.chat_repository.find_by_meeting(
            user_id,
            meeting.id,
            ChatType.MEETING.value,
        )
        if meeting_chat is None:
            raise NotFoundException("Meeting transcript chat not found")

        try:
            logger.info(
                "Starting meeting processing: meeting_id=%s file_path=%s requested_language=%s",
                meeting.id,
                meeting.file_path,
                meeting.language,
            )
            result = self.transcription_service.transcribe(
                default_storage.path(meeting.file_path),
                meeting.language,
            )
            self.message_repository.create_for_chat(
                chat_id=meeting_chat.id,
                role=ChatRole.ASSISTANT.value,
                content=result.text,
                user_id=user_id,
            )
            self.meeting_repository.complete_transcription(
                meeting.id,
                result.language,
                result.duration,
                user_id,
            )
            logger.info(
                "Meeting processing completed: meeting_id=%s detected_language=%s duration=%s",
                meeting.id,
                result.language,
                result.duration,
            )
        except Exception as exc:
            logger.exception(
                "Meeting processing failed: meeting_id=%s exception=%s",
                meeting.id,
                type(exc).__name__,
            )
            self.meeting_repository.update_status(
                meeting.id,
                MeetingStatus.FAILED.value,
                user_id,
            )
            if isinstance(exc, ApplicationException):
                raise
            raise ApplicationException("Meeting transcription failed") from exc
