from __future__ import annotations

import logging
import os
import tempfile
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename

from app.DTO.MeetingDTO import MeetingImportDTO, MeetingRecordStartDTO
from app.DTO.meeting_dtos import MeetingListFilterDTO
from app.Enums.ChatType import ChatType
from app.Enums.MeetingSourceType import MeetingSourceType
from app.Enums.MeetingStatus import MeetingStatus
from app.Exceptions import ApplicationException, NotFoundException, ValidationException
from app.Helpers.transcript import count_unique_speakers
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Repositories.Contracts.ChatRepository import ChatRepository
from app.Repositories.Contracts.MeetingRepository import MeetingRepository
from app.Services.Contracts.MeetingService import MeetingService
from app.Services.Contracts.MeetingJobService import MeetingJobService
from app.Services.Contracts.MeetingTranscriptionService import MeetingTranscriptionService


logger = logging.getLogger(__name__)


class MeetingServiceImpl(MeetingService):
    ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4", ".mov"}
    RECORDING_EXTENSIONS = ALLOWED_EXTENSIONS | {".webm", ".ogg"}

    def __init__(
        self,
        meeting_repository: MeetingRepository,
        chat_repository: ChatRepository,
        message_repository: ChatMessageRepository,
        job_service: MeetingJobService,
        transcription_service: MeetingTranscriptionService,
    ) -> None:
        self.meeting_repository = meeting_repository
        self.chat_repository = chat_repository
        self.message_repository = message_repository
        self.job_service = job_service
        self.transcription_service = transcription_service

    def import_meeting(self, user_id: int, dto: MeetingImportDTO) -> Dict[str, Any]:
        self._validate_upload(dto)
        storage_path = self._store_meeting_file(dto.source_file)

        meeting = self.meeting_repository.create_upload(
            {
                "user_id": user_id,
                "title": dto.title,
                "source_type": MeetingSourceType.UPLOAD.value,
                "file_name": dto.source_file.name,
                "file_path": storage_path,
                "file_size": int(getattr(dto.source_file, "size", 0) or 0),
                "duration": dto.duration,
                "language": dto.language or None,
                "status": MeetingStatus.PROCESSING.value,
                "created_uid": user_id,
                "updated_uid": user_id,
            }
        )
        meeting_chat, general_chat = self._create_meeting_chats(meeting, user_id)

        try:
            task_id = self.job_service.enqueue(meeting.id, user_id)
        except ApplicationException as exc:
            logger.warning("Meeting transcription queue failed for meeting %s: %s", meeting.id, exc)
            meeting = self.meeting_repository.update_status(
                meeting.id,
                MeetingStatus.FAILED.value,
                user_id,
            ) or meeting
            task_id = None

        return {
            "meeting": self._meeting_to_dict(meeting),
            "meeting_chat": self._chat_to_dict(meeting_chat, transcript=""),
            "general_chat": self._chat_to_dict(general_chat),
            "task_id": task_id,
        }

    def start_recording(self, user_id: int, dto: MeetingRecordStartDTO) -> Dict[str, Any]:
        meeting = self.meeting_repository.create_upload(
            {
                "user_id": user_id,
                "title": dto.title,
                "source_type": MeetingSourceType.RECORD.value,
                "file_name": None,
                "file_path": None,
                "file_size": 0,
                "duration": None,
                "language": dto.language or None,
                "status": MeetingStatus.PROCESSING.value,
                "created_uid": user_id,
                "updated_uid": user_id,
            }
        )
        meeting_chat, general_chat = self._create_meeting_chats(meeting, user_id)
        return {
            "meeting": self._meeting_to_dict(meeting),
            "meeting_chat": self._chat_to_dict(meeting_chat, transcript=""),
            "general_chat": self._chat_to_dict(general_chat),
        }

    def transcribe_recording_chunk(self, meeting_id: int, user_id: int, chunk) -> Dict[str, Any]:
        meeting = self.meeting_repository.find_by_id_for_user(meeting_id, user_id)
        if meeting is None:
            raise NotFoundException("Meeting not found")
        if chunk is None:
            raise ValidationException("Audio chunk is required")

        suffix = Path(chunk.name).suffix.lower() or ".webm"
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
                temporary_path = temporary_file.name
                for data in chunk.chunks():
                    temporary_file.write(data)
            result = self.transcription_service.transcribe_live_chunk(
                temporary_path,
                meeting.language,
            )
            return {"text": result.text, "language": result.language, "duration": result.duration}
        finally:
            if temporary_path and os.path.exists(temporary_path):
                os.unlink(temporary_path)

    def finish_recording(self, meeting_id: int, user_id: int, source_file) -> Dict[str, Any]:
        meeting = self.meeting_repository.find_by_id_for_user(meeting_id, user_id)
        if meeting is None:
            raise NotFoundException("Meeting not found")
        if source_file is None:
            raise ValidationException("Final recording file is required")
        extension = Path(source_file.name).suffix.lower()
        if extension not in self.RECORDING_EXTENSIONS:
            raise ValidationException("Unsupported recording file type")

        storage_path = self._store_meeting_file(source_file)
        meeting = self.meeting_repository.update_recording_file(
            meeting.id,
            source_file.name,
            storage_path,
            int(getattr(source_file, "size", 0) or 0),
            user_id,
        ) or meeting
        task_id = self.job_service.enqueue(meeting.id, user_id)
        meeting_chat = self.chat_repository.find_by_meeting(user_id, meeting.id, ChatType.MEETING.value)
        general_chat = self.chat_repository.find_by_meeting(user_id, meeting.id, ChatType.GENERAL.value)
        return {
            "meeting": self._meeting_to_dict(meeting),
            "meeting_chat": self._chat_to_dict(meeting_chat, transcript="") if meeting_chat else None,
            "general_chat": self._chat_to_dict(general_chat) if general_chat else None,
            "task_id": task_id,
        }

    def list(
        self,
        user_id: int,
        filters: Optional[MeetingListFilterDTO] = None,
    ) -> List[Dict[str, Any]]:
        filters = filters or MeetingListFilterDTO()
        start_date = self._parse_filter_date(filters.start_date, "startDate")
        end_date = self._parse_filter_date(filters.end_date, "endDate")
        if start_date and end_date and start_date > end_date:
            raise ValidationException("startDate must be before or equal to endDate")

        meetings = self.meeting_repository.list_by_user(
            user_id,
            search=filters.search,
            start_date=start_date,
            end_date=end_date,
        )
        meetings = list(meetings)
        speaker_counts = self.message_repository.speaker_counts_by_meeting(
            user_id,
            [meeting.id for meeting in meetings],
        )
        return [
            self._meeting_to_dict(meeting, speaker_counts.get(meeting.id, 0))
            for meeting in meetings
        ]

    def get_detail(self, meeting_id: int, user_id: int) -> Dict[str, Any]:
        meeting = self.meeting_repository.find_by_id_for_user(meeting_id, user_id)
        if meeting is None:
            raise NotFoundException("Meeting not found")

        meeting_chat = self.chat_repository.find_by_meeting(
            user_id,
            meeting.id,
            ChatType.MEETING.value,
        )
        general_chat = self.chat_repository.find_by_meeting(
            user_id,
            meeting.id,
            ChatType.GENERAL.value,
        )
        transcript_messages = list(self.message_repository.list_by_chat(meeting_chat.id)) if meeting_chat else []
        transcript = "\n\n".join(message.content for message in transcript_messages if message.content)
        speaker_count = count_unique_speakers(message.content for message in transcript_messages)

        return {
            "meeting": self._meeting_to_dict(meeting, speaker_count),
            "meeting_chat": self._chat_to_dict(meeting_chat, transcript=transcript) if meeting_chat else None,
            "general_chat": self._chat_to_dict(general_chat) if general_chat else None,
            "transcript": transcript,
        }

    def delete(self, meeting_id: int, user_id: int) -> bool:
        if not self.meeting_repository.soft_delete(meeting_id, user_id):
            raise NotFoundException("Meeting not found")
        return True

    def _validate_upload(self, dto: MeetingImportDTO) -> None:
        if dto.source_file is None:
            raise ValidationException("Meeting file is required")

        extension = Path(dto.source_file.name).suffix.lower()
        if extension not in self.ALLOWED_EXTENSIONS:
            raise ValidationException("Unsupported meeting file type")

    @staticmethod
    def _parse_filter_date(value: str, field_name: str) -> date | None:
        if not value:
            return None
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise ValidationException(f"{field_name} must use YYYY-MM-DD format") from exc

    def _store_meeting_file(self, source_file) -> str:
        file_name = get_valid_filename(source_file.name)
        return default_storage.save(f"meetings/{file_name}", source_file)

    def _create_meeting_chats(self, meeting, user_id: int):
        meeting_chat = self.chat_repository.create_for_meeting(
            user_id=user_id,
            meeting_id=meeting.id,
            title=f"{meeting.title} Transcript",
            chat_type=ChatType.MEETING.value,
        )
        general_chat = self.chat_repository.create_for_meeting(
            user_id=user_id,
            meeting_id=meeting.id,
            title=f"{meeting.title} AI Assistant",
            chat_type=ChatType.GENERAL.value,
        )
        return meeting_chat, general_chat

    def _meeting_to_dict(self, meeting, speaker_count: int = 0) -> Dict[str, Any]:
        return {
            "id": meeting.id,
            "user_id": meeting.user_id,
            "title": meeting.title,
            "source_type": meeting.source_type,
            "file_name": meeting.file_name,
            "file_path": meeting.file_path,
            "file_size": meeting.file_size,
            "duration": meeting.duration,
            "language": meeting.language,
            "status": meeting.status,
            "speaker_count": speaker_count,
            "created_at": meeting.created_at,
        }

    def _chat_to_dict(self, chat, transcript: str | None = None) -> Dict[str, Any]:
        data = {
            "id": chat.id,
            "user_id": chat.user_id,
            "meeting_id": chat.meeting_id,
            "title": chat.title,
            "type": chat.type,
        }
        if transcript is not None:
            data["transcript"] = transcript
        return data
