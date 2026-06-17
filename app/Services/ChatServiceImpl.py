import logging
from typing import Any

from app.DTO.ChatDTO import ChatCreateDTO, ChatMessageCreateDTO, ChatUpdateDTO
from app.Enums.ChatRole import ChatRole
from app.Exceptions import ApplicationException, NotFoundException, ValidationException
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository
from app.Repositories.Contracts.ChatRepository import ChatRepository
from app.Services.Contracts.ChatAttachmentContentService import ChatAttachmentContentService
from app.Services.Contracts.ChatMessageAttachmentService import ChatMessageAttachmentService
from app.Services.Contracts.ChatService import ChatService
from app.Services.Contracts.GeminiService import GeminiService


logger = logging.getLogger(__name__)


class ChatServiceImpl(ChatService):
    def __init__(
        self,
        chat_repository: ChatRepository,
        message_repository: ChatMessageRepository,
        attachment_service: ChatMessageAttachmentService,
        attachment_content_service: ChatAttachmentContentService,
        gemini_service: GeminiService,
    ) -> None:
        self.chat_repository = chat_repository
        self.message_repository = message_repository
        self.attachment_service = attachment_service
        self.attachment_content_service = attachment_content_service
        self.gemini_service = gemini_service

    def create(self, user_id: int, dto: ChatCreateDTO) -> dict[str, Any]:
        chat = self.chat_repository.create_for_user(user_id=user_id, title=dto.title)
        return self._chat_to_dict(chat)

    def list(self, user_id: int) -> list[dict[str, Any]]:
        return [self._chat_to_dict(chat) for chat in self.chat_repository.list_by_user(user_id)]

    def get_detail(self, chat_id: int, user_id: int) -> dict[str, Any]:
        chat = self._get_owned_chat(chat_id, user_id)
        messages = list(self.message_repository.list_by_chat(chat.id))
        attachments_by_message = self.attachment_service.group_by_message_ids(
            [message.id for message in messages],
        )
        return {
            **self._chat_to_dict(chat),
            "messages": [
                self._message_to_dict(message, attachments_by_message.get(message.id, []))
                for message in messages
            ],
        }

    def get_message_detail(self, chat_id: int, user_id: int, message_id: int) -> dict[str, Any]:
        chat = self._get_owned_chat(chat_id, user_id)
        message = self.message_repository.find_by_id_for_chat(message_id, chat.id)
        if message is None:
            raise NotFoundException("Message not found")
        attachments = self.attachment_service.list_by_message(message.id)
        return self._message_to_dict(message, attachments)

    def update(self, chat_id: int, user_id: int, dto: ChatUpdateDTO) -> dict[str, Any]:
        if not dto.title:
            raise ValidationException("Title is required")

        chat = self.chat_repository.update_for_user(chat_id, user_id, dto.title)
        if chat is None:
            raise NotFoundException("Chat not found")
        return self._chat_to_dict(chat)

    def delete(self, chat_id: int, user_id: int) -> bool:
        deleted = self.chat_repository.soft_delete(chat_id, user_id)
        if not deleted:
            raise NotFoundException("Chat not found")
        return True

    def send_message(self, chat_id: int, user_id: int, dto: ChatMessageCreateDTO) -> dict[str, Any]:
        if not dto.message and not dto.attachments:
            raise ValidationException("Message or attachments is required")

        chat = self._get_owned_chat(chat_id, user_id)
        previous_history = [
            self._message_to_dict(message)
            for message in self.message_repository.list_by_chat(chat.id)
        ]

        user_message = self.message_repository.create_for_chat(
            chat_id=chat.id,
            role=ChatRole.USER.value,
            content=dto.message,
            user_id=user_id,
        )
        user_attachments = self.attachment_service.create_many(
            chat_message_id=user_message.id,
            attachments=dto.attachments,
            user_id=user_id,
        )
        gemini_prompt, attachment_parts = self.attachment_content_service.build_gemini_input(dto)
        try:
            assistant_content = self.gemini_service.generate_response(
                gemini_prompt,
                previous_history,
                attachment_parts,
            )
        except ApplicationException as exc:
            logger.warning("Gemini response failed: %s", exc)
            assistant_content = (
                "Sorry, I could not generate a response right now. "
                "Please try again in a moment."
            )
        assistant_message = self.message_repository.create_for_chat(
            chat_id=chat.id,
            role=ChatRole.ASSISTANT.value,
            content=assistant_content,
            user_id=user_id,
        )

        return {
            "user_message": self._message_to_dict(user_message, user_attachments),
            "assistant_message": self._message_to_dict(assistant_message, []),
        }

    def _get_owned_chat(self, chat_id: int, user_id: int):
        chat = self.chat_repository.find_by_id_for_user(chat_id, user_id)
        if chat is None:
            raise NotFoundException("Chat not found")
        return chat

    def _chat_to_dict(self, chat) -> dict[str, Any]:
        return {
            "id": chat.id,
            "title": chat.title,
        }

    def _message_to_dict(self, message, attachments: list[dict[str, Any]] | None = None) -> dict[str, Any]:
        return {
            "id": message.id,
            "chat_id": message.chat_id,
            "role": message.role,
            "message": message.content,
            "content": message.content,
            "attachments": attachments or [],
        }
