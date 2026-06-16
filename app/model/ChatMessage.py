from django.db import models

from app.model.BaseModel import BaseModel


class ChatMessage(BaseModel):
    chat_id = models.BigIntegerField()
    role = models.CharField(max_length=20)  # user, assistant
    content = models.TextField()

    class Meta:
        app_label = "app"
        db_table = "chat_messages"

    def __str__(self) -> str:
        return f"{self.role}: {self.content[:50]}"