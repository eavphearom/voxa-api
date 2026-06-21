from abc import ABC, abstractmethod


class MeetingProcessingService(ABC):
    @abstractmethod
    def process(self, meeting_id: int, user_id: int) -> None:
        raise NotImplementedError
