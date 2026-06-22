from __future__ import annotations

from datetime import datetime, timezone
from types import SimpleNamespace

from django.test import SimpleTestCase

from app.Enums.ChatType import ChatType
from app.Helpers.transcript import count_unique_speakers
from app.Services.MeetingServiceImpl import MeetingServiceImpl


class SpeakerCountTests(SimpleTestCase):
    def test_counts_only_unique_speaker_labels(self):
        transcript = """Speaker 1:
Hello

Speaker 2:
Hi

Speaker 1:
Welcome back"""

        self.assertEqual(count_unique_speakers([transcript]), 2)

    def test_counts_speakers_across_multiple_transcript_records(self):
        contents = ["Speaker 1:\nHello", "Speaker 2:\nHi", "Speaker 1:\nAgain"]

        self.assertEqual(count_unique_speakers(contents), 2)

    def test_returns_zero_without_transcripts(self):
        self.assertEqual(count_unique_speakers([]), 0)

    def test_meeting_detail_includes_unique_speaker_count(self):
        meeting = SimpleNamespace(
            id=13,
            user_id=7,
            title="chines",
            source_type="upload",
            file_name="meeting.mp4",
            file_path="meetings/meeting.mp4",
            file_size=100,
            duration=22,
            language="zh",
            status="completed",
            created_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
        )
        transcript_chat = SimpleNamespace(
            id=20,
            user_id=7,
            meeting_id=13,
            title="Transcript",
            type=ChatType.MEETING.value,
        )
        meeting_repository = SimpleNamespace(
            find_by_id_for_user=lambda meeting_id, user_id: meeting,
        )
        chat_repository = SimpleNamespace(
            find_by_meeting=lambda user_id, meeting_id, chat_type: (
                transcript_chat if chat_type == ChatType.MEETING.value else None
            ),
        )
        message_repository = SimpleNamespace(
            list_by_chat=lambda chat_id: [
                SimpleNamespace(content="Speaker 1:\nHello\n\nSpeaker 2:\nHi\n\nSpeaker 1:\nAgain")
            ],
        )
        service = MeetingServiceImpl(
            meeting_repository,
            chat_repository,
            message_repository,
            None,
            None,
        )

        result = service.get_detail(13, 7)

        self.assertEqual(result["meeting"]["speaker_count"], 2)
