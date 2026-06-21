from django.utils import timezone

from app.model import Chat
from app.Repositories.Contracts.ChatRepository import ChatRepository


class ChatRepositoryImpl(ChatRepository):
    def create_for_user(self, user_id: int, title: str) -> Chat:
        return Chat.objects.create(
            user_id=user_id,
            title=title,
            type="general",
            created_uid=user_id,
            updated_uid=user_id,
        )

    def create_for_meeting(self, user_id: int, meeting_id: int, title: str, chat_type: str) -> Chat:
        return Chat.objects.create(
            user_id=user_id,
            meeting_id=meeting_id,
            title=title,
            type=chat_type,
            created_uid=user_id,
            updated_uid=user_id,
        )

    def find_by_meeting(self, user_id: int, meeting_id: int, chat_type: str) -> Chat | None:
        return Chat.objects.filter(
            user_id=user_id,
            meeting_id=meeting_id,
            type=chat_type,
            is_deleted=False,
        ).order_by("id").first()

    def list_by_user(self, user_id: int):
        return Chat.objects.filter(
            user_id=user_id,
            type="general",
            meeting_id__isnull=True,
            is_deleted=False,
        ).order_by("-updated_at", "-created_at")

    def find_by_id_for_user(self, chat_id: int, user_id: int) -> Chat | None:
        return Chat.objects.filter(id=chat_id, user_id=user_id, is_deleted=False).first()

    def update_for_user(self, chat_id: int, user_id: int, title: str) -> Chat | None:
        chat = self.find_by_id_for_user(chat_id, user_id)
        if chat is None:
            return None

        chat.title = title
        chat.updated_uid = user_id
        chat.save(update_fields=["title", "updated_uid", "updated_at"])
        return chat

    def soft_delete(self, chat_id: int, user_id: int) -> bool:
        chat = self.find_by_id_for_user(chat_id, user_id)
        if chat is None:
            return False

        chat.is_deleted = True
        chat.deleted_at = timezone.now()
        chat.deleted_uid = user_id
        chat.updated_uid = user_id
        chat.save(update_fields=["is_deleted", "deleted_at", "deleted_uid", "updated_uid", "updated_at"])
        return True
