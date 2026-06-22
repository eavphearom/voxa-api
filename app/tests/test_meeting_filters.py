from datetime import date, datetime, timezone
from types import SimpleNamespace

from django.test import SimpleTestCase

from app.DTO.meeting_dtos import MeetingListFilterDTO
from app.Exceptions import ValidationException
from app.Services.MeetingServiceImpl import MeetingServiceImpl


class FakeMeetingRepository:
    def __init__(self):
        self.filters = None

    def list_by_user(self, user_id, search="", start_date=None, end_date=None):
        self.filters = (user_id, search, start_date, end_date)
        return [
            SimpleNamespace(
                id=1,
                user_id=user_id,
                title="Weekly planning",
                source_type="record",
                file_name=None,
                file_path=None,
                file_size=0,
                duration=60,
                language="en",
                status="completed",
                created_at=datetime(2026, 6, 21, tzinfo=timezone.utc),
            )
        ]


class FakeMessageRepository:
    def __init__(self, speaker_counts=None):
        self.speaker_counts = speaker_counts or {}

    def speaker_counts_by_meeting(self, user_id, meeting_ids):
        return self.speaker_counts


class MeetingFilterTests(SimpleTestCase):
    def setUp(self):
        self.repository = FakeMeetingRepository()
        self.message_repository = FakeMessageRepository({1: 2})
        self.service = MeetingServiceImpl(
            self.repository,
            None,
            self.message_repository,
            None,
            None,
        )

    def test_passes_search_and_inclusive_date_range_to_repository(self):
        filters = MeetingListFilterDTO(
            search="planning",
            start_date="2026-05-22",
            end_date="2026-06-21",
        )

        result = self.service.list(7, filters)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["speaker_count"], 2)
        self.assertEqual(
            self.repository.filters,
            (7, "planning", date(2026, 5, 22), date(2026, 6, 21)),
        )

    def test_rejects_invalid_date_order(self):
        filters = MeetingListFilterDTO(start_date="2026-06-21", end_date="2026-05-22")

        with self.assertRaisesMessage(
            ValidationException,
            "startDate must be before or equal to endDate",
        ):
            self.service.list(7, filters)

    def test_rejects_invalid_date_format(self):
        with self.assertRaisesMessage(ValidationException, "startDate must use YYYY-MM-DD format"):
            self.service.list(7, MeetingListFilterDTO(start_date="05/22/2026"))
