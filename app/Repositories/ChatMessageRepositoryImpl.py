from app.model import ChatMessage
from app.Repositories.BaseRepositoryImpl import BaseRepositoryImpl
from app.Repositories.Contracts.ChatMessageRepository import ChatMessageRepository


class ChatMessageRepositoryImpl(BaseRepositoryImpl, ChatMessageRepository):
    model = ChatMessage

    def get_all(self):
        return ChatMessage.objects.filter(is_deleted=False).order_by("created_at", "id")

    def get_by_id(self, object_id: int):
        return ChatMessage.objects.filter(id=object_id, is_deleted=False).first()

    def create_for_chat(
        self,
        chat_id: int,
        role: str,
        content: str,
        user_id: int | None = None,
    ) -> ChatMessage:
        return ChatMessage.objects.create(
            chat_id=chat_id,
            role=role,
            content=content,
            created_uid=user_id,
            updated_uid=user_id,
        )

    def list_by_chat(self, chat_id: int):
        return ChatMessage.objects.filter(chat_id=chat_id, is_deleted=False).order_by("created_at", "id")

    def delete(self, object_id: int) -> bool:
        message = self.get_by_id(object_id)
        if message is None:
            return False
        message.is_deleted = True
        message.save(update_fields=["is_deleted", "updated_at"])
        return True
