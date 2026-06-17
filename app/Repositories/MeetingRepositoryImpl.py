from app.model import Meeting
from app.Repositories.BaseRepositoryImpl import BaseRepositoryImpl
from app.Repositories.Contracts.MeetingRepository import MeetingRepository


class MeetingRepositoryImpl(BaseRepositoryImpl, MeetingRepository):
    model = Meeting
