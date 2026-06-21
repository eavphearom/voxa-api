from django.db import models

from app.Enums.ChatType import ChatType
from app.model.BaseModel import BaseModel


class Chat(BaseModel):
    user_id = models.BigIntegerField()
    title = models.CharField(max_length=255, default="New Chat")
    type = models.CharField(
        max_length=20,
        choices=[(item.value, item.value) for item in ChatType],
        default=ChatType.GENERAL.value,
    )
    meeting_id = models.BigIntegerField(null=True, blank=True)

    class Meta:
        app_label = "app"
        db_table = "chats"

    def __str__(self) -> str:
        return self.title
