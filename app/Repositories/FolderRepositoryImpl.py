from django.utils import timezone

from app.model import Folder, FolderMeeting, Meeting
from app.Repositories.Contracts.FolderRepository import FolderRepository


class FolderRepositoryImpl(FolderRepository):
    def create_for_user(self, user_id: int, name: str) -> Folder:
        return Folder.objects.create(
            user_id=user_id,
            name=name,
            created_uid=user_id,
            updated_uid=user_id,
        )

    def list_by_user(self, user_id: int):
        return Folder.objects.filter(user_id=user_id, is_deleted=False).order_by("name", "id")

    def find_by_id_for_user(self, folder_id: int, user_id: int) -> Folder | None:
        return Folder.objects.filter(id=folder_id, user_id=user_id, is_deleted=False).first()

    def update_for_user(self, folder_id: int, user_id: int, name: str) -> Folder | None:
        folder = self.find_by_id_for_user(folder_id, user_id)
        if folder is None:
            return None
        folder.name = name
        folder.updated_uid = user_id
        folder.save(update_fields=["name", "updated_uid", "updated_at"])
        return folder

    def soft_delete(self, folder_id: int, user_id: int) -> bool:
        folder = self.find_by_id_for_user(folder_id, user_id)
        if folder is None:
            return False
        folder.is_deleted = True
        folder.deleted_at = timezone.now()
        folder.deleted_uid = user_id
        folder.updated_uid = user_id
        folder.save(update_fields=["is_deleted", "deleted_at", "deleted_uid", "updated_uid", "updated_at"])
        FolderMeeting.objects.filter(folder_id=folder.id, is_deleted=False).update(
            is_deleted=True,
            deleted_at=timezone.now(),
            deleted_uid=user_id,
            updated_uid=user_id,
        )
        return True

    def add_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> FolderMeeting:
        link = FolderMeeting.objects.filter(folder_id=folder_id, meeting_id=meeting_id).first()
        if link is None:
            return FolderMeeting.objects.create(
                folder_id=folder_id,
                meeting_id=meeting_id,
                created_uid=user_id,
                updated_uid=user_id,
            )
        if link.is_deleted:
            link.is_deleted = False
            link.deleted_at = None
            link.deleted_uid = None
            link.updated_uid = user_id
            link.save(update_fields=["is_deleted", "deleted_at", "deleted_uid", "updated_uid", "updated_at"])
        return link

    def remove_meeting(self, folder_id: int, meeting_id: int, user_id: int) -> bool:
        link = FolderMeeting.objects.filter(
            folder_id=folder_id,
            meeting_id=meeting_id,
            is_deleted=False,
        ).first()
        if link is None:
            return False
        link.is_deleted = True
        link.deleted_at = timezone.now()
        link.deleted_uid = user_id
        link.updated_uid = user_id
        link.save(update_fields=["is_deleted", "deleted_at", "deleted_uid", "updated_uid", "updated_at"])
        return True

    def list_meetings(self, folder_id: int):
        meeting_ids = FolderMeeting.objects.filter(
            folder_id=folder_id,
            is_deleted=False,
        ).values_list("meeting_id", flat=True)
        return Meeting.objects.filter(id__in=meeting_ids, is_deleted=False).order_by("-created_at")
