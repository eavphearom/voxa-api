from abc import ABC, abstractmethod


class MeetingJobService(ABC):
    @abstractmethod
    def enqueue(self, meeting_id: int, user_id: int) -> str:
        raise NotImplementedError
