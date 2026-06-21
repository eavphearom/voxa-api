from django.db import models

from app.Enums.AttachmentType import AttachmentType
from app.model.BaseModel import BaseModel
from app.model.ChatMessage import ChatMessage


class ChatMessageAttachment(BaseModel):
    chat_message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name="attachments",
    )
    attachment_type = models.CharField(
        max_length=20,
        choices=[(item.value, item.value) for item in AttachmentType],
    )
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1000)
    file_size = models.BigIntegerField()

    class Meta:
        app_label = "app"
        db_table = "chat_message_attachments"

    def __str__(self) -> str:
        return self.file_name
