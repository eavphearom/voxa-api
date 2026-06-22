from __future__ import annotations

from typing import List

from django.utils import timezone

from app.model import ChatMessageAttachment
from app.Repositories.BaseRepositoryImpl import BaseRepositoryImpl
from app.Repositories.Contracts.ChatMessageAttachmentRepository import ChatMessageAttachmentRepository


class ChatMessageAttachmentRepositoryImpl(BaseRepositoryImpl, ChatMessageAttachmentRepository):
    model = ChatMessageAttachment

    def get_all(self):
        return ChatMessageAttachment.objects.filter(is_deleted=False).order_by("created_at", "id")

    def get_by_id(self, object_id: int):
        return ChatMessageAttachment.objects.filter(id=object_id, is_deleted=False).first()

    def create_for_message(
        self,
        chat_message_id: int,
        data: dict,
        user_id: int | None = None,
    ) -> ChatMessageAttachment:
        return ChatMessageAttachment.objects.create(
            chat_message_id=chat_message_id,
            attachment_type=data["attachment_type"],
            file_name=data["file_name"],
            file_path=data["file_path"],
            file_size=data["file_size"],
            created_uid=user_id,
            updated_uid=user_id,
        )

    def list_by_message(self, chat_message_id: int):
        return ChatMessageAttachment.objects.filter(
            chat_message_id=chat_message_id,
            is_deleted=False,
        ).order_by("created_at", "id")

    def list_by_messages(self, chat_message_ids: List[int]):
        return ChatMessageAttachment.objects.filter(
            chat_message_id__in=chat_message_ids,
            is_deleted=False,
        ).order_by("created_at", "id")

    def soft_delete(self, attachment_id: int, user_id: int | None = None) -> bool:
        attachment = self.get_by_id(attachment_id)
        if attachment is None:
            return False

        attachment.is_deleted = True
        attachment.deleted_at = timezone.now()
        attachment.deleted_uid = user_id
        attachment.updated_uid = user_id
        attachment.save(update_fields=["is_deleted", "deleted_at", "deleted_uid", "updated_uid", "updated_at"])
        return True

    def delete(self, object_id: int) -> bool:
        return self.soft_delete(object_id)
