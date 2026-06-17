from typing import Any

from django.core.files.storage import default_storage
from django.utils.text import get_valid_filename

from app.DTO.ChatMessageAttachmentDTO import ChatMessageAttachmentDTO
from app.Exceptions import NotFoundException
from app.Repositories.Contracts.ChatMessageAttachmentRepository import ChatMessageAttachmentRepository
from app.Services.Contracts.ChatMessageAttachmentService import ChatMessageAttachmentService


class ChatMessageAttachmentServiceImpl(ChatMessageAttachmentService):
    def __init__(self, repository: ChatMessageAttachmentRepository) -> None:
        self.repository = repository

    def create_many(
        self,
        chat_message_id: int,
        attachments: list[ChatMessageAttachmentDTO],
        user_id: int | None = None,
    ) -> list[dict[str, Any]]:
        created = [
            self.repository.create_for_message(
                chat_message_id=chat_message_id,
                data=self._store_attachment(chat_message_id, attachment),
                user_id=user_id,
            )
            for attachment in attachments
        ]
        return [self._to_dict(attachment) for attachment in created]

    def list_by_message(self, chat_message_id: int) -> list[dict[str, Any]]:
        return [
            self._to_dict(attachment)
            for attachment in self.repository.list_by_message(chat_message_id)
        ]

    def group_by_message_ids(self, chat_message_ids: list[int]) -> dict[int, list[dict[str, Any]]]:
        grouped: dict[int, list[dict[str, Any]]] = {}
        if not chat_message_ids:
            return grouped

        for attachment in self.repository.list_by_messages(chat_message_ids):
            grouped.setdefault(attachment.chat_message_id, []).append(self._to_dict(attachment))
        return grouped

    def soft_delete(self, attachment_id: int, user_id: int | None = None) -> bool:
        deleted = self.repository.soft_delete(attachment_id, user_id)
        if not deleted:
            raise NotFoundException("Attachment not found")
        return True

    def _to_dict(self, attachment) -> dict[str, Any]:
        return {
            "id": attachment.id,
            "chat_message_id": attachment.chat_message_id,
            "attachment_type": attachment.attachment_type,
            "file_name": attachment.file_name,
            "file_path": attachment.file_path,
            "file_size": attachment.file_size,
        }

    def _store_attachment(
        self,
        chat_message_id: int,
        attachment: ChatMessageAttachmentDTO,
    ) -> dict[str, Any]:
        file_name = get_valid_filename(attachment.file_name)
        storage_path = default_storage.save(
            f"chat_messages/{chat_message_id}/{file_name}",
            attachment.uploaded_file,
        )
        return {
            "attachment_type": attachment.attachment_type.value,
            "file_name": attachment.file_name,
            "file_path": storage_path,
            "file_size": attachment.file_size,
        }
