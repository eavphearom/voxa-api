from django.db import models

from app.model.BaseModel import BaseModel


class Chat(BaseModel):
    user_id = models.BigIntegerField()
    title = models.CharField(max_length=255, default="New Chat")

    class Meta:
        app_label = "app"
        db_table = "chats"

    def __str__(self) -> str:
        return self.title