from app.Enums.ChatType import ChatType
from app.Helpers.transcript import count_unique_speakers
from app.model import Chat, ChatMessage
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

    def speaker_counts_by_meeting(self, user_id: int, meeting_ids: list[int]) -> dict[int, int]:
        if not meeting_ids:
            return {}

        transcript_chats = list(
            Chat.objects.filter(
                user_id=user_id,
                meeting_id__in=meeting_ids,
                type=ChatType.MEETING.value,
                is_deleted=False,
            ).values_list("id", "meeting_id")
        )
        chat_to_meeting = {chat_id: meeting_id for chat_id, meeting_id in transcript_chats}
        contents_by_meeting = {meeting_id: [] for meeting_id in meeting_ids}

        messages = ChatMessage.objects.filter(
            chat_id__in=chat_to_meeting,
            is_deleted=False,
        ).values_list("chat_id", "content")
        for chat_id, content in messages:
            contents_by_meeting[chat_to_meeting[chat_id]].append(content)

        return {
            meeting_id: count_unique_speakers(contents)
            for meeting_id, contents in contents_by_meeting.items()
        }

    def find_by_id_for_chat(self, message_id: int, chat_id: int) -> ChatMessage | None:
        return ChatMessage.objects.filter(id=message_id, chat_id=chat_id, is_deleted=False).first()

    def delete(self, object_id: int) -> bool:
        message = self.get_by_id(object_id)
        if message is None:
            return False
        message.is_deleted = True
        message.save(update_fields=["is_deleted", "updated_at"])
        return True
